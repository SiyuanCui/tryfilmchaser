from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Issues
from common.utils import input
from common import utils, models as commonModels


# Create your views here.

def getWhere(request, qs):
    orderby = input(request, "order", "id")
    sort = input(request, "sort", "DESC").upper()
    if sort == "DESC":
        qs = qs.order_by("-" + orderby)
    else:
        qs = qs.order_by(orderby)

    return qs


# Administrator list page
def adminlist(request):
    qs = getWhere(request, Issues.objects)

    qs = qs.all()
    # paged
    pagesize = input(request, "pagesize", 12)
    # Get data by page
    paginator = Paginator(qs, pagesize)
    # Get the current page number, which is 1 by default
    page = request.GET.get('page', 1)
    try:
        list = paginator.page(page)
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

    return render(request, "issues/admin/list.html", locals(), )


# Comment list page
def author(request):
    qs = getWhere(request, Issues.objects)
    qs = qs.filter(pinglunren=request.session['username'])

    qs = qs.all()
    pagesize = input(request, "pagesize", 12)
    paginator = Paginator(qs, pagesize)
    # Get the current page number, which is 1 by default
    page = request.GET.get('page', 1)
    try:
        list = paginator.page(page)  # 分页
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    is_paginated = True if paginator.num_pages > 1 else False
    page_range = paginator.get_elided_page_range(page, on_each_side=3, on_ends=2)
    page = list

    orderby = input(request, "order", "id")
    sort = input(request, "sort", "DESC").upper()

    # context = {'list': list, 'page': list, 'paginator': paginator,
    #           'is_paginated': is_paginated,'page_range': page_range }

    return render(request, "issues/admin/add.html", locals(), )


# Front add page
def add(request):
    if not utils.checkLogin(request):
        return utils.showError(request, "Please login first.");

    return render(request, "issues/add.html", locals())


def adminupdt(request):
    id = request.GET.get("id")
    mmm = Issues.objects.get(pk=id)
    if mmm == None:
        return utils.showError(request, "No data found")

    return render(request, "issues/admin/updt.html", locals())


def delete(request):
    ids = request.GET.getlist("id")

    for id in ids:
        map = Issues.objects.get(pk=id)

        try:
            commonModels.execute(
                "update movies set issues_count=(select count(*) from issues where tableid='%s' ),score=(select avg(score) from issues where tableid='%s' ) where id='%s'" % (
                    map.tableid, map.tableid, map.tableid))
        except Exception as e:
            print("%s" % (e))

        map.delete()

    return utils.showSuccess(request, "Deleted.")

    return utils.showSuccess(request, "Success.")


def insert(request):
    if not utils.checkLogin(request):
        return utils.showError(request, "Please login first.");

    post = request.POST.copy()
    data = {
        'table': utils.input(request, 'table', ''),
        # movie id
        'tableid': utils.input(request, 'id', ''),

        'title': utils.input(request, 'title', ''),
        'score': utils.input(request, 'score', ''),
        'content': utils.input(request, 'content', ''),
        'author': utils.input(request, 'author', ''),

    }
    if data['tableid'] == '':
        data['tableid'] = 0
    else:
        data['tableid'] = int(data['tableid'])
    if data['author'] == '':
        data['author'] = utils.session(request, "name")

    model = Issues(**data)
    model.save(force_insert=True)

    try:
        commonModels.execute(
            "update movies set issues_count=(select count(*) from issues where tableid='%s' ),score=(select avg(score) from issues where tableid='%s' ) where id='%s'" % (
                request.POST.get("tableid"), request.POST.get("tableid"), request.POST.get("tableid")))
    except Exception as e:
        print("%s" % (e))

    referer = utils.input(request, "referer", request.headers.get('referer'))

    return utils.showSuccess(request, "Comments posted successfully！", referer)


def update(request):
    charuid = request.POST.get('id')
    post = request.POST.copy()
    old = Issues.objects.get(pk=charuid)
    data = {
        'id': charuid,
        'table': utils.input(request, 'table', old.table),
        'tableid': utils.input(request, 'id', '').strip(),
        'title': utils.input(request, 'title', old.title),
        'score': utils.input(request, 'score', old.score),
        'content': utils.input(request, 'content', old.content),
        'author': utils.input(request, 'author', old.author),
        'addtime': old.addtime,

    }

    if data['tableid'] == '':
        data['tableid'] = 0
    else:
        data['tableid'] = int(data['tableid'])

    model = Issues(**data)
    model.save(force_update=True)

    referer = utils.input(request, "referer", request.headers.get('referer'))
    return utils.showSuccess(request, "Modification successful.", referer)