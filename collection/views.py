from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from collection.models import Collection
from common.utils import input
from common import utils, models as commonModels


# Create your views here.

def getWhere(request, qs):
    if request.GET.get("title"):
        qs = qs.filter(title__contains=request.GET.get("title"))

    orderby = input(request, "order", "id")
    sort = input(request, "sort", "DESC").upper()
    if sort == "DESC":
        qs = qs.order_by("-" + orderby)
    else:
        qs = qs.order_by(orderby)

    return qs


# Administrator list page
def adminlist(request):
    qs = getWhere(request, Collection.objects)

    qs = qs.all()
    pagesize = input(request, "pagesize", 12)
    paginator = Paginator(qs, pagesize)
    page = request.GET.get('page', 1)
    try:
        list = paginator.page(page)  # paging
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    is_paginated = True if paginator.num_pages > 1 else False
    page_range = paginator.get_elided_page_range(page, on_each_side=3, on_ends=2)

    orderby = input(request, "order", "id")
    sort = input(request, "sort", "DESC").upper()
    page = list

    # context = {'list': list, 'page': list, 'paginator': paginator,
    #           'is_paginated': is_paginated,'page_range': page_range }

    return render(request, "collection/admin/list.html", locals(), )


def username(request):
    qs = getWhere(request, Collection.objects)
    qs = qs.filter(username=request.session['username'])

    qs = qs.all()
    pagesize = input(request, "pagesize", 12)
    paginator = Paginator(qs, pagesize)
    page = request.GET.get('page', 1)
    try:
        list = paginator.page(page)  # paging
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    is_paginated = True if paginator.num_pages > 1 else False
    page_range = paginator.get_elided_page_range(page, on_each_side=3, on_ends=2)
    page = list

    orderby = input(request, "order", "id")
    sort = input(request, "sort", "DESC").upper()

    return render(request, "collection/admin/username.html", locals(), )


# 前台添加页面
def add(request):
    if not utils.checkLogin(request):
        return utils.showError(request, "请登录后操作");

    return render(request, "collection/add.html", locals())


def delete(request):
    ids = request.GET.getlist("id")

    for id in ids:
        map = Collection.objects.get(pk=id)

        try:
            commonModels.execute(
                "update movies set collection_count=(select count(*) from collection where tableid='%s' ) where id='%s'" % (
                map.movie_id, map.movie_id))
        except Exception as e:
            print("%s" % (e))

        map.delete()

    return utils.showSuccess(request, "Delete succeeded")


def batch(request):
    ids = request.POST.getlist("ids")

    if "delete" in request.POST:
        for id in ids:
            map = Collection.objects.get(pk=id)
            commonModels.execute(
                "update movies set collection_count=(select count(*) from collection where tableid='%s' ) where id='%s'" % (
                map.movie_id, map.movie_id))
            map.delete()

    return utils.showSuccess(request, "批量处理成功")


def insert(request):
    if not utils.checkLogin(request):
        return utils.showError(request, "请登录后操作");

    post = request.POST.copy()
    data = {
        'username': utils.input(request, 'username', ''),
        'movie_id': utils.input(request, 'movie_id', ''),
        'relation_tabel': utils.input(request, 'table', ''),
        'title': utils.input(request, 'title', ''),

    }
    if data['username'] == '':
        data['username'] = utils.session(request, "username")
    if data['movie_id'] == '':
        data['movie_id'] = 0
    else:
        data['movie_id'] = int(data['movie_id'])

    res = Collection.objects.filter(relation_tabel=utils.input(request, "table")).filter(
        movie_id=utils.input(request, "movie_id")).filter(username=utils.session(request, "username")).all();
    if len(res):
        res[0].delete()

        try:
            commonModels.execute(
                "update movies set collection_count=(select count(*) from collection where movie_id='%s' ) where id='%s'" % (
                    utils.input(request, "movie_id"), utils.input(request, "movie_id")))
        except Exception as e:
            print("%s" % (e))

        return utils.showSuccess(request, "已取消收藏")

    model = Collection(**data)
    model.save(force_insert=True)

    try:
        commonModels.execute(
            "update movies set collection_count=(select count(*) from collection where movie_id='%s' ) where id='%s'" % (
            utils.input(request, "movie_id"), utils.input(request, "movie_id")))
    except Exception as e:
        print("%s" % (e))

    referer = utils.input(request, "referer", request.headers.get('referer'))

    return utils.showSuccess(request, "Successfully added", referer)


def update(request):
    charuid = request.POST.get('id')
    post = request.POST.copy()
    old = Collection.objects.get(pk=charuid)
    data = {
        'id': charuid,
        'username': utils.input(request, 'username', old.username),
        'movie_id': utils.input(request, 'movie_id', '').strip(),
        'table': utils.input(request, 'table', old.table),
        'title': utils.input(request, 'title', old.title),
        'addtime': old.addtime,

    }

    if data['movie_id'] == '':
        data['movie_id'] = 0
    else:
        data['movie_id'] = int(data['movie_id'])

    model = Collection(**data)
    model.save(force_update=True)

    referer = utils.input(request, "referer", request.headers.get('referer'))
    return utils.showSuccess(request, "Modified successfully", referer)
