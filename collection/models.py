from django.db import models
from common import models as commonModels
from django.contrib.auth import models as authModels


# Create your models here.


class Collection(models.Model):
    username = models.CharField('username', db_column='username', max_length=50, default='')
    movie_id = models.IntegerField('movie_id', default=0)
    table = models.CharField('table', max_length=50, default='')
    title = models.CharField('title', max_length=255, default='')
    addtime = models.DateTimeField('addtime', auto_now_add=True)

    class Meta:
        db_table = 'collection'
        verbose_name = 'collection'  # 单数形式
        verbose_name_plural = verbose_name  # 复数形式
