from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Columns
from common.utils import input
from common import utils,models as commonModels




# Create your views here.

def getWhere(request,qs):
    if request.GET.get("name"):
        qs = qs.filter(name__contains=request.GET.get("name"))




    orderby = input(request, "order", "id")
    sort = input(request, "sort", "DESC").upper()
    if sort == "DESC":
        qs = qs.order_by("-" + orderby)
    else:
        qs = qs.order_by(orderby)

    return qs


def adminlist(request):
    qs = getWhere(request,Columns.objects)

    qs = qs.all()
    pagesize = input(request, "pagesize", 12)
    paginator = Paginator(qs, pagesize)
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

    #context = {'list': list, 'page': list, 'paginator': paginator,
    #           'is_paginated': is_paginated,'page_range': page_range }

    return render(request , "columns/admin/list.html" , locals() , )




#Add page in the background
def adminadd(request):

    return render(request , "columns/admin/add.html",locals())






def adminupdt(request):
    id = request.GET.get("id")
    mmm = Columns.objects.get(pk = id)
    if mmm == None:
        return utils.showError(request,"No relevant data found")


    return render(request, "columns/admin/updt.html" , locals())







def delete(request):
    ids = request.GET.getlist("id")

    for id in ids:
        map = Columns.objects.get(pk = id)

        map.delete()

    return utils.showSuccess(request,"Delete succeeded")

def insert(request):

    post = request.POST.copy()
    data = {
        'name': utils.input(request,'name',''),

    }


    model = Columns(**data)
    model.save(force_insert = True)

    referer = utils.input(request,"referer" , request.headers.get('referer'))

    return utils.showSuccess(request , "Successfully added" , referer)

def update(request):
    id = request.POST.get('id')
    post = request.POST.copy()
    old = Columns.objects.get(pk = id)
    data = {
        'id': id,
        'name': utils.input(request,'name', old.name),

    }



    model = Columns(**data)
    model.save(force_update = True)

    referer = utils.input(request , "referer" , request.headers.get('referer'))
    return utils.showSuccess(request , "Modified successfully" , referer)



