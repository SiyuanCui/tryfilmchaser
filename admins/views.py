from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Admins
from common.utils import input
from common import utils, models as commonModels


# Create your views here.

def getWhere(request, qs):
    if request.GET.get("username"):
        qs = qs.filter(username__contains=request.GET.get("username"))

    orderby = input(request, "order", "id")
    sort = input(request, "sort", "DESC").upper()
    if sort == "DESC":
        qs = qs.order_by("-" + orderby)
    else:
        qs = qs.order_by(orderby)

    return qs


def adminlist(request):
    qs = getWhere(request, Admins.objects)

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

    return render(request, "admins/admin/list.html", locals(), )


def adminadd(request):
    return render(request, "admins/admin/add.html", locals())


def adminupdt(request):
    id = request.GET.get("id")
    mmm = Admins.objects.get(pk=id)
    if mmm == None:
        return utils.showError(request, "No relevant data found")

    return render(request, "admins/admin/updt.html", locals())


def adminupdtself(request):
    id = request.session['id']
    mmm = Admins.objects.get(pk=id)
    if mmm == None:
        return utils.showError(request, "No relevant data found")

    return render(request, "admins/admin/updtself.html", locals())


def delete(request):
    ids = request.GET.getlist("id")

    for id in ids:
        map = Admins.objects.get(pk=id)

        map.delete()

    return utils.showSuccess(request, "Delete succeeded")

    return utils.showSuccess(request, "Batch processing succeeded")


def insert(request):
    post = request.POST.copy()
    data = {
        'username': utils.input(request, 'username', ''),
        'password': utils.input(request, 'pwd', ''),

    }

    model = Admins(**data)
    model.save(force_insert=True)

    referer = utils.input(request, "referer", request.headers.get('referer'))

    return utils.showSuccess(request, "Successfully added", referer)


def update(request):
    id = request.POST.get('id')
    post = request.POST.copy()
    old = Admins.objects.get(pk=id)
    data = {
        'id': id,
        'username': utils.input(request, 'username', old.username),
        'password': utils.input(request, 'pwd', old.password),

    }

    model = Admins(**data)
    model.save(force_update=True)

    referer = utils.input(request, "referer", request.headers.get('referer'))
    return utils.showSuccess(request, "Modified successfully", referer)
