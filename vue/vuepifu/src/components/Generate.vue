<template>
<div class="showdemo">
    <h1 @mouseover="showImage" @mouseout="hideImage">开始生成</h1>
    <img v-if="isHovered" :src="imageSrc" alt="Hovered Image" class="hovered_image"/>
</div>
<!--    <div><p @click="uploadimg">上传啊</p></div>-->
  <div class="generatebox">
      <div class="showimgbox">
          <div class="uploadbox">
              <input type="file" @change="onFileChange">
              <el-button type="primary" @click="uploadimg">上传图片</el-button>
              <el-button type="primary" @click="deleteData">清空图片</el-button>
              <el-button type="primary" @click="executeScript">生成</el-button>
          </div>
          <div class="imgbox">
              <div  v-for="(item,index) in imageUrl" :key="index"  class="singleimg">
<!--                  <p>看看啊！！+item.img_url</p>-->
              <img :src="'http://127.0.0.1:8000/img/'+item.img_url" alt="#">
              </div>
          </div>
      </div>
      <div ref="sceneCanvas" class="sceneCanvas" v-loading="isLoading">
          <div class="downloadbtn" v-if="finishLoading">
            <el-button type="primary" @click="saveAsOBJ" >保存OBJ</el-button>
            <el-button type="primary" @click="saveScreenshot">保存截图</el-button>
          </div>
      </div>
      <div class="addbgbtn" v-if="finishLoading">
          <el-button type="primary" v-for="item in bgitems" :key="item.id" @click="addbg(item)" class="singlebgbtn">{{ item.name }}</el-button>
      </div>
  </div>
<!--    <div class="mask" v-show="showobjflag" :key="componentcount"></div>-->
</template>

<script lang="ts" setup>
import axios from "axios";
import {ref, onMounted, onBeforeMount, watchEffect} from 'vue';
import {OBJLoader} from "@/assets/three/loaders/OBJLoader.mjs";
import {OrbitControls} from "@/assets/three/controls/OrbitControls.mjs";
import {saveAs} from "file-saver"
import {OBJExporter} from "@/assets/three/examples/jsm/exporters/OBJExporter"
import html2canvas from 'html2canvas';

const finishLoading = ref(false);
const isLoading = ref(false);
const file = ref(null);
const imageUrl = ref(null)
const ifshowimg = ref(true)
const isHovered = ref(false);
const imageSrc = ref('http://127.0.0.1:8000/img/background/demo.jpg');
let scene = null;
let renderer = null;
let camera = null;
let bgloader = null;
let texture = null;

// const animate = ref(null);
// let showobjflag = ref(true)
// let componentcount = reactive({value : 0})
const onFileChange = (event) => {
    file.value = event.target.files[0];
    // console.log(file.value.name);
};
// 上传图片函数
const uploadimg = () => {
    const formData = new FormData();
    formData.append('file', file.value);
    axios.post('http://127.0.0.1:8000/pifuvueweb/demo',formData,{
        headers:{
            'Content-Type': 'multipart/form-data'
        }
    }).then((response) => {
        imageUrl.value = response.data.images;
        // console.log(response.data);
    }).catch((error) => {
        console.log(error);
    });
};
// 加载3D模型
const executeScript = async () => {
    isLoading.value = true;
    try {
        const response = await axios.post('http://127.0.0.1:8000/pifuvueweb/generate');
        // result.value = response.data.result;
        console.log(response);
    } catch (error) {
        // 处理错误
        console.error(error);
    } finally {
        isLoading.value = false;
        finishLoading.value = true;
        console.log('123');
    }
    addmodel();
};

const sceneCanvas = ref(null);
const addmodel=() => {
    const canvasWidth = sceneCanvas.value.clientWidth*1.2;
    const canvasHeight = sceneCanvas.value.clientHeight;
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, canvasWidth / canvasHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(canvasWidth, canvasHeight);
    renderer.setClearColor(0xffffff);
    sceneCanvas.value.appendChild(renderer.domElement);
    const controls = new OrbitControls(camera, renderer.domElement)
    const objloader = new OBJLoader()
    objloader.load('http://127.0.0.1:8000/img/results/results/result_0_0_00.obj', (obj) => {
        const scale = 20
        obj.scale.set(scale, scale, scale)
        obj.position.set(0,-15,-10)
        scene.add(obj);
    });
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(1, 1, 1);
    scene.add(ambientLight);
    scene.add(directionalLight);
    camera.position.z = 50;
    camera.aspect = canvasWidth / canvasHeight;
    controls.enableDamping = true
    controls.dampingFactor = 0.05
    controls.rotateSpeed = 0.5
    const animate = () => {
        requestAnimationFrame(animate);
        renderer.render(scene,camera);
    }
    animate();
}

// 删除上传内容
const deleteData = () => {
    axios.post('http://127.0.0.1:8000/pifuvueweb/delete').then((response) => {
        console.log(response.data.message);
    }).catch((error) => {
        console.error(error)
    })
    window.location.reload();
}

//保存OBJ文件
const saveAsOBJ = () => {
    const url = 'http://127.0.0.1:8000/img/results/results/result_0_0_00.obj'
    const link = document.createElement('a');
    link.href = url;
    link.download = 'model.obj';
    link.click();
    window.URL.revokeObjectURL(url);
}

// 保存截图
const saveScreenshot = () => {
    renderer.render(scene,camera);
    const screenshotDataUrl = renderer.domElement.toDataURL('image/png');

// 创建下载链接并设置截图数据
    const link = document.createElement('a');
    link.href = screenshotDataUrl;
    link.download = 'screenshot.png';

// 触发点击下载链接
    link.click();
}

const addbg = (item) => {
    bgloader = new THREE.TextureLoader();
    texture = bgloader.load('http://127.0.0.1:8000/img/background/'+item.name+'.webp',() =>{
        const rt = new THREE.WebGLCubeRenderTarget(texture.image.height)
        // texture.repeat.set(100,100);
        rt.fromEquirectangularTexture(renderer, texture)
        scene.background = rt.texture
    })
}

const bgitems = ([
    {id: 1, name: 'seaside', info: 'seaside'},
    {id: 2, name: 'museum', info: 'museum'},
])

const showImage = () => {
    isHovered.value = true;
};
const hideImage = () => {
    isHovered.value = false;
};
</script>

<style scoped>

</style>