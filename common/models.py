from django.db import models
from .widgets import UMeditorWidget, MyImageWidget, MyImagesWidget, MyPaperWidget
from django.db import connection


# Create your models here.


def execute(sql):
    print(sql)
    cursor = None
    reCount = False
    try:
        cursor = connection.cursor()
        reCount = cursor.execute(sql)
        connection.commit()
        cursor.close()

    except Exception as e:
        print(e)
        if cursor != None:
            cursor.close()

    return reCount


def select(sql):
    cursor = None
    result = []
    try:
        print(sql)
        cursor = connection.cursor()
        reCount = cursor.execute(sql)
        col_names = [row[0] for row in cursor.description]
        if reCount:
            alls = cursor.fetchall()
            for v in alls:
                re = dict(zip(col_names, v))
                result.append(re)
        cursor.close()
    except Exception as e:
        print(e)
        if cursor != None:
            cursor.close()
    print(result)
    return result

    # rs = RawTable.objects.raw(sql)
    # return rs


def find(sql):
    cursor = None
    result = dict()
    try:
        print(sql)
        cursor = connection.cursor()
        reCount = cursor.execute(sql)
        col_names = [row[0] for row in cursor.description]
        if reCount:
            result = dict(zip(col_names, cursor.fetchone()))
        cursor.close()
    except Exception as e:
        print(e)
        if cursor != None:
            cursor.close()
    print(result)
    return result


def findOne(sql):
    cursor = None
    result = 0
    try:
        print(sql)
        cursor = connection.cursor()
        reCount = cursor.execute(sql)

        if reCount:
            re = cursor.fetchone()
            result = re[0]
        cursor.close()
    except Exception as e:
        print(e)
        if cursor != None:
            cursor.close()
    print(result)
    return result


class UMeditorField(models.TextField):

    def formfield(self, **kwargs):
        defaults = {'widget': UMeditorWidget}
        defaults.update(kwargs)
        return super(UMeditorField, self).formfield(**defaults)


class MyImageField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 255
        super(MyImageField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'widget': MyImageWidget}
        defaults.update(kwargs)
        return super(MyImageField, self).formfield(**defaults)


class MyImagesField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {'widget': MyImagesWidget}
        defaults.update(kwargs)
        return super(MyImagesField, self).formfield(**defaults)


class MyPaperField(models.Model):
    _default_hint = ('dict', '[]')
    empty_strings_allowed = False

    def __init__(self, *, verbose_name=None, name=None, type='leixing', danxuanti='', duoxuanti='', panduanti='',
                 **kwargs):
        defaults = {
            verbose_name: verbose_name,
            name: name,
            type: type,
            danxuanti: danxuanti,
            duoxuanti: duoxuanti,
            panduanti: panduanti
        }
        kwargs["verbose_name"] = verbose_name
        kwargs["name"] = name

        super(MyPaperField, self).__init__(defaults, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'widget': MyPaperWidget}
        defaults.update(kwargs)
        return super(MyPaperField, self).formfield(**defaults)
