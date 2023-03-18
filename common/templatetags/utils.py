from django import template

register = template.Library()
from common import models
from common import utils


@register.simple_tag(name='sql')
def sql(sql, type, *args):
    if len(args):
        if type == 'select':
            return models.select(sql % args)
        else:
            return models.find(sql % args)
    else:
        if type == 'select':
            return models.select(sql)
        else:
            return models.find(sql)


@register.simple_tag(name='getID')
def getID():
    return utils.getID()


@register.simple_tag(name='query')
def query(table, type, *args):
    className = utils.parseName(table)
    model = utils.imports(table + ".models", className)

    qs = model.objects
    i = 0
    length = len(args)
    filters = {}
    limit = 0
    while (i < length):
        cmd = args[i]
        if cmd == "filter":
            key = args[i + 1]
            value = args[i + 2]
            i = i + 2
            filters[key] = value
        elif cmd == "limit":
            key = args[i + 1]
            i = i + 1
            limit = int(key)
        elif cmd == "order":
            key = args[i + 1]
            qs = qs.order_by(key)
            i = i + 1
        i = i + 1
    pass

    if len(filters):
        qs = qs.filter(**filters)

    if limit:
        list = qs.all()[0:limit]
    else:
        list = qs.all()

    if type == "select":
        return list
    elif type == "find":
        if len(list) > 0:
            return list[0]
        return {}
    elif type == "page":
        # 分页查询
        return list

    return []


@register.simple_tag(name='images')
def images(val):
    arr = val.split(',')
    if arr[0]:
        return arr[0]
    return ""
