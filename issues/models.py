from django.db import models
from common import models as commonModels
from django.contrib.auth import models as authModels


# Create your models here.


class Issues(models.Model):
    table = models.CharField('tabel', max_length=50, default='')
    tableid = models.IntegerField('tableid', default=0)
    title = models.CharField('title', max_length=255, default='')
    score = models.CharField('score', max_length=255, default='')
    content = models.TextField('content', default='')
    author = models.CharField('author', db_column='author', max_length=50, default='')
    addtime = models.DateTimeField('addtime', auto_now_add=True)

    class Meta:
        db_table = 'issues'
        verbose_name = 'issue'  # 单数形式
        verbose_name_plural = verbose_name  # 复数形式
