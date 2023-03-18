from django.db import models
from common import models as commonModels
from django.contrib.auth import models as authModels

# Create your models here.


class Admins(models.Model):
    username = models.CharField('username' , max_length = 50,default='')
    password = models.CharField('password' , max_length = 128,default='')



    class Meta:
        db_table = 'admins'
        verbose_name = 'admin'
        verbose_name_plural = verbose_name





