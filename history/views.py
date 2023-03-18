from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import History
from common.utils import input
from common import utils,models as commonModels


from movies.models import Movies
from columns.models import Columns

# Create your views here.

def getWhere(request,qs):
    if request.GET.get("moviesid"):
        qs = qs.filter(moviesid=request.GET.get("moviesid"))
    if request.GET.get("title"):
        qs = qs.filter(title__contains=request.GET.get("title"))
    if request.GET.get("column"):
        qs = qs.filter(column=request.GET.get("column"))




    orderby = input(request, "order", "id")
    sort = input(request, "sort", "DESC").upper()
    if sort == "DESC":
        qs = qs.order_by("-" + orderby)
    else:
        qs = qs.order_by(orderby)

    return qs


# Browse people list page
def visitor(request):
    qs = getWhere(request,History.objects)
    qs = qs.filter(visitor=request.session['username'])

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
    page = list

    orderby = input(request, "order", "id")
    sort = input(request, "sort", "DESC").upper()

    #context = {'list': list, 'page': list, 'paginator': paginator,
    #           'is_paginated': is_paginated,'page_range': page_range }

    return render(request , "history/admin/visitor.html" , locals() , )






# 前台添加页面
def add(request):
    if not utils.checkLogin(request):
        return utils.showError(request,"Please operate after logging in")


    if 'id' in request.GET:
        id = request.GET.get('id')
        readMap = Movies.objects.get(pk = id)

    return render(request, "history/add.html", locals())











def delete(request):
    ids = request.GET.getlist("id")

    for id in ids:
        map = History.objects.get(pk = id)

        map.delete()

    return utils.showSuccess(request,"Delete succeeded")



def insert(request):
    if not utils.checkLogin(request):
        return utils.showError(request,"Please operate after logging in")

    post = request.POST.copy()
    data = {
        'moviesid': utils.input(request,'moviesid',utils.input(request,'moviesid',0)),
        'title': utils.input(request,'title',''),
        'column': utils.input(request,'column',utils.input(request,'column',0)),
        'visitor': utils.input(request,'visitor',''),

    }
    if data['visitor'] == '':
        data['visitor'] = utils.session(request, "username")


    model = History(**data)
    model.save(force_insert = True)

    referer = utils.input(request,"referer" , request.headers.get('referer'))

    return utils.showSuccess(request , "Successfully added" , referer)

def update(request):
    id = request.POST.get('id')
    post = request.POST.copy()
    old = History.objects.get(pk = id)
    data = {
        'id': id,
        'moviesid': utils.input(request,'moviesid',utils.input(request,'moviesid',0)),
        'title': utils.input(request,'title', old.title),
        'column': utils.input(request,'column',utils.input(request,'column',0)),
        'visitor': utils.input(request,'visitor', old.visitor),
        'addtime': old.addtime,

    }



    model = History(**data)
    model.save(force_update = True)

    referer = utils.input(request , "referer" , request.headers.get('referer'))
    return utils.showSuccess(request , "Modified successfully" , referer)



