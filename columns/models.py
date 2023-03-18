from django.db import models
from common import models as commonModels
from django.contrib.auth import models as authModels


# Create your models here.


class Columns(models.Model):
    name = models.CharField('name', max_length=255, default='')

    class Meta:
        db_table = 'columns'
        verbose_name = 'columns'  # 单数形式
        verbose_name_plural = verbose_name  # 复数形式
