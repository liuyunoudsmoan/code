import sys
import os

from numpy.lib.function_base import select

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import time
import json
import numpy as np
import torch
from torch.utils.data import DataLoader

# createmask
import os
from PIL import Image
import requests


from lib.options import BaseOptions
from lib.mesh_util import *
from lib.sample_util import *
from lib.train_util import *
from lib.model import *

from PIL import Image
import torchvision.transforms as transforms
import glob
import tqdm


# createmask
def process_jpg_files(folder_path):
    # 获取文件夹中所有的 JPG 文件列表
    jpg_files = [file for file in os.listdir(folder_path) if file.endswith(".jpg")]

    for file in jpg_files:
        # 构建文件的完整路径
        file_path = os.path.join(folder_path, file)

        # 调用 Remove.bg API 移除背景
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(file_path, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': 'aynoitcGZW41x3PepjUhni1N'},
        )

        if response.status_code == requests.codes.ok:
            # 保存移除背景后的图像
            output_path = os.path.join(folder_path, f"output_{file}")
            with open(output_path, 'wb') as out:
                out.write(response.content)

            # 打开透明背景图像
            input_image = Image.open(output_path)

            # 创建一个新的图像，大小和透明背景图像一致，背景为黑色
            output_image = Image.new("RGB", input_image.size, (0, 0, 0))

            # 获取透明背景图像的像素数据
            pixels = input_image.load()

            # 遍历每个像素
            for i in range(input_image.size[0]):
                for j in range(input_image.size[1]):
                    # 获取当前像素的RGBA值
                    r, g, b, a = pixels[i, j]

                    # 如果透明度大于0，说明是人体部分，将其替换为白色
                    if a > 0:
                        output_image.putpixel((i, j), (255, 255, 255))

            # 保存结果图像为 PNG 格式
            mask_path = os.path.join(folder_path, f"{file.split('.')[0]}_mask.png")
            output_image.save(mask_path, format='PNG')

            print(f"Processed file: {file}")
        else:
            print(f"Error processing file: {file}")


def delete_output_files(folder_path):
    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)

    # 遍历文件夹中的每个文件
    for file in files:
        # 检查文件名是否以 "output" 开头并且是文件（不是文件夹）
        if file.startswith("output") and os.path.isfile(os.path.join(folder_path, file)):
            # 构建文件的完整路径并删除
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
            print(f"Deleted file: {file}")

# get options
opt = BaseOptions().parse()

class Evaluator:
    def __init__(self, opt, projection_mode='orthogonal'):
        self.opt = opt
        self.load_size = self.opt.loadSize
        self.to_tensor = transforms.Compose([
            transforms.Resize(self.load_size),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        # set cuda
        cuda = torch.device('cuda:%d' % opt.gpu_id) if torch.cuda.is_available() else torch.device('cpu')

        # create net
        netG = HGPIFuNet(opt, projection_mode).to(device=cuda)
        print('Using Network: ', netG.name)

        if opt.load_netG_checkpoint_path:
            netG.load_state_dict(torch.load(opt.load_netG_checkpoint_path, map_location=cuda))

        if opt.load_netC_checkpoint_path is not None:
            print('loading for net C ...', opt.load_netC_checkpoint_path)
            netC = ResBlkPIFuNet(opt).to(device=cuda)
            netC.load_state_dict(torch.load(opt.load_netC_checkpoint_path, map_location=cuda))
        else:
            netC = None

        os.makedirs(opt.results_path, exist_ok=True)
        os.makedirs('%s/%s' % (opt.results_path, opt.name), exist_ok=True)

        opt_log = os.path.join(opt.results_path, opt.name, 'opt.txt')
        with open(opt_log, 'w') as outfile:
            outfile.write(json.dumps(vars(opt), indent=2))

        self.cuda = cuda
        self.netG = netG
        self.netC = netC
    
    def load_image(self, images, masks):
        # Name
        img_name = os.path.splitext(os.path.basename(images[0]))[0]
        # Calib
        B_MIN = np.array([-1, -1, -1])
        B_MAX = np.array([1, 1, 1])
        projection_matrix = np.identity(4)
        projection_matrix[1, 1] = -1
        
        # modify: multi-view setting
        calibList = []
        if self.opt.num_views == 1:
            calibList.append(torch.Tensor(projection_matrix).float())
        elif self.opt.num_views == 3:
            extrin_60 = np.array([
                [-0.5, 0, 0.866, 0], 
                [0, 1, 0, 0],
                [-0.866, 0, -0.5, 0], 
                [0, 0, 0, 1]
            ])
            extrin_120 = np.array([
                [-0.5, 0, -0.866, 0], 
                [0, 1, 0, 0],
                [0.866, 0, -0.5, 0], 
                [0, 0, 0, 1]
            ])
            calibList.append(torch.Tensor(projection_matrix).float())
            calibList.append(torch.Tensor(np.matmul(projection_matrix, extrin_60)).float())
            calibList.append(torch.Tensor(np.matmul(projection_matrix, extrin_120)).float())
        elif self.opt.num_views == 4:
            extrin_90 = np.array([
                [0, 0, 1, 0], 
                [0, 1, 0, 0],
                [-1, 0, 0, 0], 
                [0, 0, 0, 1]
            ])
            extrin_180 = np.array([
                [-1, 0, 0, 0], 
                [0, 1, 0, 0],
                [0, 0, -1, 0], 
                [0, 0, 0, 1]
            ])
            extrin_270 = np.array([
                [0, 0, -1, 0], 
                [0, 1, 0, 0],
                [1, 0, 0, 0], 
                [0, 0, 0, 1]
            ])
            calibList.append(torch.Tensor(projection_matrix).float())
            calibList.append(torch.Tensor(np.matmul(projection_matrix, extrin_90)).float())
            calibList.append(torch.Tensor(np.matmul(projection_matrix, extrin_180)).float())
            calibList.append(torch.Tensor(np.matmul(projection_matrix, extrin_270)).float())
        # Mask
        maskList = []
        imageList = []
        for mask, image in zip(masks, images):
            mask = Image.open(mask).convert('L')
            mask = transforms.Resize(self.load_size)(mask)
            mask = transforms.ToTensor()(mask).float()
            maskList.append(mask)
            image = Image.open(image).convert('RGB')
            image = self.to_tensor(image)
            image = mask.expand_as(image) * image
            imageList.append(image)
        return {
            'name': img_name,
            'img': torch.stack(imageList, dim=0),
            'calib': torch.stack(calibList, dim=0),
            'mask': torch.stack(maskList, dim=0),
            'b_min': B_MIN,
            'b_max': B_MAX,
        }
        #--------------------------------------#

    def eval(self, data, use_octree=False):
        '''
        Evaluate a data point
        :param data: a dict containing at least ['name'], ['image'], ['calib'], ['b_min'] and ['b_max'] tensors.
        :return:
        '''
        opt = self.opt
        with torch.no_grad():
            self.netG.eval()
            if self.netC:
                self.netC.eval()
            save_path = '%s/%s/result_%s.obj' % (opt.results_path, opt.name, data['name'])
            if self.netC:
                gen_mesh_color(opt, self.netG, self.netC, self.cuda, data, save_path, use_octree=use_octree)
            else:
                gen_mesh(opt, self.netG, self.cuda, data, save_path, use_octree=use_octree)


if __name__ == '__main__':
    evaluator = Evaluator(opt)
    print('123131231312')
    # createmask
    folder_path = opt.test_folder_path
    process_jpg_files(folder_path)
    delete_output_files(folder_path)


    # modify: multi-view setting #
    test_images = [opt.test_folder_path+'/0_0_00.jpg', opt.test_folder_path+'/90_0_00.jpg', opt.test_folder_path+'/180_0_00.jpg', opt.test_folder_path+'/270_0_00.jpg']
    test_masks = [opt.test_folder_path+'/0_0_00_mask.png', opt.test_folder_path+'/90_0_00_mask.png', opt.test_folder_path+'/180_0_00_mask.png', opt.test_folder_path+'/270_0_00_mask.png']

    print("Use view:", opt.num_views)

    try:
        data = evaluator.load_image(test_images, test_masks)
        evaluator.eval(data, True)
    except Exception as e:
        print("error:", e.args)
