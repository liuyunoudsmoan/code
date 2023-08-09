from django.db import models

# Create your models here.
class Img(models.Model):
    img_url = models.ImageField(upload_to='img')
    img_name = models.CharField(max_length=1000,default=' ')
