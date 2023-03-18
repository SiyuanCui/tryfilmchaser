from django.db import models
from common import models as commonModels
from django.contrib.auth import models as authModels


# Create your models here.


class Movies(models.Model):
    id = models.CharField('id', max_length=10, primary_key=True)
    title = models.CharField('title', max_length=255, null=False)
    column = models.IntegerField(default=1, db_column='column', )
    director = models.CharField('director', max_length=50, default='')
    actor = models.TextField('actor', default='')
    date = models.CharField('date', max_length=10, default='')
    video = models.FileField('video', default='')
    pic = commonModels.MyImageField('pic', default='')
    tags = models.TextField('tags', default='')
    collection_count = models.IntegerField('collection_count', default=0)
    visit_count = models.IntegerField('visit_count', default=0)
    issues_count = models.IntegerField('issues_count', default=0)
    score = models.DecimalField('score', default=0, max_digits=16, decimal_places=2)
    intro = commonModels.UMeditorField('intro', default='', max_length=4096)
    addtime = models.DateTimeField('addtime', auto_now_add=True)
    #
    imdb = models.URLField(max_length=128)
    time_length = models.CharField(max_length=128)

    class Meta:
        db_table = 'movies'
        verbose_name = 'movies'  # 单数形式
        verbose_name_plural = verbose_name  # 复数形式
