from django.db import models
from common import models as commonModels
from django.contrib.auth import models as authModels

# Create your models here.
 


class History(models.Model):
    moviesid = models.ForeignKey('movies.Movies', verbose_name='movie id', default=1, on_delete=models.CASCADE, db_column='moviesid', editable=False, related_name="history_movie_id")
    title = models.CharField('title', max_length = 255, default='')
    column = models.ForeignKey('columns.Columns', default=1, db_column='column', on_delete=models.CASCADE, related_name="history_columns_id")
    visitor = models.CharField('visitor', db_column='visitor', max_length=50, default='')
    addtime = models.DateTimeField('addtime' , auto_now_add=True)



    class Meta:
        db_table = 'history'
        verbose_name = 'History'  #singular form
        verbose_name_plural = verbose_name #Plural form





