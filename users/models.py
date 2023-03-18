from django.db import models
from common import models as commonModels
from django.contrib.auth import models as authModels

# Create your models here.
SEX_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),

)


class Users(models.Model):
    username = models.CharField('username', max_length=50, default='')
    password = models.CharField('password', max_length=128, default='')
    name = models.CharField('name', max_length=50, default='')
    sex = models.CharField('sex', choices=SEX_CHOICES, max_length=8, default='')
    mobile = models.CharField('mobile', max_length=50, default='')
    email = models.CharField('email', max_length=50, default='')
    idcard = models.CharField('idcard', max_length=50, default='')
    photo = commonModels.MyImageField('photo', default='')

    class Meta:
        db_table = 'users'
        verbose_name = 'user'  # 单数形式
        verbose_name_plural = verbose_name  # 复数形式
