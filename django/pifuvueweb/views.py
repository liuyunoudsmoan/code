from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from rest_framework import  viewsets
# from .serializers import userDetailSerializer, userSerializer
from rest_framework.response import Response
from rest_framework import status
import pifuvueweb.models as models
from django.http import JsonResponse
from django.conf import settings
from subprocess import Popen, PIPE
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from .models import user
# from user import serializers
# import pandas as pd
import numpy as np

# from sklearn import preprocessing

import numpy as np
import os

class test(viewsets.ViewSet):
    def list(self, request):
        print('123')
        return Response(status=status.HTTP_200_OK)


    def upload(self, request):
        if request.method == 'POST':
            file = models.Img(img_url= request.FILES.get('file'))
            file.save()
            images = list(models.Img.objects.all().values())
            context = {
                'images': images
            }
            # print(context)
            return JsonResponse(context)

    def deleteData(self, request):
        models.Img.objects.all().delete()
        print('删除')
        folder_path = os.path.join(settings.MEDIA_ROOT, 'img')
        obj_path = os.path.join(settings.MEDIA_ROOT, 'results')
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            print(file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        for file_name in os.listdir(obj_path):
            file_path = os.path.join(obj_path, file_name)
            print(file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        images = list(models.Img.objects.all().values())
        context = {
            'images': images
        }
        return JsonResponse(context)

    def generate(self, request):
        images = list(models.Img.objects.all().values())
        context = {
            'images': images
        }
        script_path = os.path.join(settings.MEDIA_ROOT, 'script/apps/eval.py')
        process = Popen(['python', script_path], stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        result = output.decode('utf-8') if output else error.decode('utf-8')
        return Response(result)
