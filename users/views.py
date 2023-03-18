from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Users
from common.utils import input
from common import utils, models as commonModels


# Create your views here.

def getWhere(request, qs):
    if request.GET.get("username"):
        qs = qs.filter(username__contains=request.GET.get("username"))
    if request.GET.get("name"):
        qs = qs.filter(name__contains=request.GET.get("name"))
    if request.GET.get("sex"):
        qs = qs.filter(sex=request.GET.get("sex"))
    if request.GET.get("mobile"):
        qs = qs.filter(mobile__contains=request.GET.get("mobile"))
    if request.GET.get("idcard"):
        qs = qs.filter(idcard__contains=request.GET.get("idcard"))

    orderby = input(request, "order", "id")
    sort = input(request, "sort", "DESC").upper()
    if sort == "DESC":
        qs = qs.order_by("-" + orderby)
    else:
        qs = qs.order_by(orderby)

    return qs


# Administrator list page
def adminlist(request):
    qs = getWhere(request, Users.objects)

    qs = qs.all()
    # paged
    pagesize = input(request, "pagesize", 12)
    # Get data by page
    paginator = Paginator(qs, pagesize)
    # Get the current page number, which is 1 by default
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

    return render(request, "user/admin/list.html", locals(), )


# Add page in the background
def adminadd(request):
    return render(request, "user/admin/add.html", locals())


# 前台添加页面
def add(request):
    return render(request, "user/add.html", locals())


def adminupdt(request):
    id = request.GET.get("id")
    mmm = Users.objects.get(pk=id)
    if mmm == None:
        return utils.showError(request, "No data found.")

    return render(request, "user/admin/updt.html", locals())


def adminupdtself(request):
    id = request.session['id']
    mmm = Users.objects.get(pk=id)
    if mmm == None:
        return utils.showError(request, "No data found.")

    return render(request, "user/admin/updtself.html", locals())


def delete(request):
    ids = request.GET.getlist("id")

    for id in ids:
        map = Users.objects.get(pk=id)

        map.delete()

    return utils.showSuccess(request, "Delete successful!")

    return utils.showSuccess(request, "批量处理成功")


def insert(request):
    post = request.POST.copy()
    data = {
        'username': utils.input(request, 'username', ''),
        'password': utils.input(request, 'password', ''),
        'name': utils.input(request, 'name', ''),
        'sex': utils.input(request, 'sex', ''),
        'mobile': utils.input(request, 'mobile', ''),
        'email': utils.input(request, 'email', ''),
        'idcard': utils.input(request, 'idcard', ''),
        'photo': utils.input(request, 'photo', ''),

    }

    model = Users(**data)
    model.save(force_insert=True)

    referer = utils.input(request, "referer", request.headers.get('referer'))

    return utils.showSuccess(request, "Account create successful!", referer)


def update(request):
    charuid = request.POST.get('id')
    post = request.POST.copy()
    old = Users.objects.get(pk=charuid)
    data = {
        'id': charuid,
        'username': utils.input(request, 'username', old.username),
        'password': utils.input(request, 'password', old.password),
        'name': utils.input(request, 'name', old.name),
        'sex': utils.input(request, 'sex', old.sex),
        'mobile': utils.input(request, 'mobile', old.mobile),
        'email': utils.input(request, 'email', old.email),
        'idcard': utils.input(request, 'idcard', old.idcard),
        'photo': utils.input(request, 'photo', old.photo),

    }

    model = Users(**data)
    model.save(force_update=True)

    referer = utils.input(request, "referer", request.headers.get('referer'))
    return utils.showSuccess(request, "Modifications successful", referer)
