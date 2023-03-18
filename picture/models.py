from django.db import models
from common import models as commonModels
from django.contrib.auth import models as authModels


# Create your models here.


class Picture(models.Model):
    title = models.CharField('title', max_length=50, default='')
    image = commonModels.MyImageField('image', default='')
    url = models.CharField('url', max_length=255, default='')

    class Meta:
        db_table = 'picture'
        verbose_name = 'picture'
        verbose_name_plural = verbose_name
