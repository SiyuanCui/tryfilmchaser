from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Picture
from common.utils import input
from common import utils,models as commonModels




# Create your views here.

def getWhere(request,qs):
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
    qs = getWhere(request,Picture.objects)

    qs = qs.all()
    # paged
    pagesize = input(request, "pagesize", 12)
    # Get data by page
    paginator = Paginator(qs, pagesize)

    # Get the current page number, which is 1 by default
    page = request.GET.get('page', 1)
    page_range = paginator.get_elided_page_range(page, on_each_side=3, on_ends=2)

    try:
        list = paginator.page(page)  # paging
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    is_paginated = True if paginator.num_pages > 1 else False

    orderby = input(request, "order", "id")
    sort = input(request, "sort", "DESC").upper()
    page = list

    #context = {'list': list, 'page': list, 'paginator': paginator,
    #           'is_paginated': is_paginated,'page_range': page_range }

    return render(request , "picture/admin/list.html" , locals()  )




#Add page in the background
def adminadd(request):

    return render(request , "picture/admin/add.html",locals())






def adminupdt(request):
    id = request.GET.get("id")
    mmm = Picture.objects.get(pk = id)
    if mmm == None:
        return utils.showError(request,"No relevant data found")


    return render(request, "picture/admin/updt.html" , locals())







def delete(request):
    ids = request.GET.getlist("id")

    for id in ids:
        map = Picture.objects.get(pk = id)

        map.delete()

    return utils.showSuccess(request,"Delete succeeded")



def insert(request):

    post = request.POST.copy()
    data = {
        'title': utils.input(request,'title',''),
        'image': utils.input(request,'image',''),
        'url': utils.input(request,'url',''),

    }


    model = Picture(**data)
    model.save(force_insert = True)

    referer = utils.input(request,"referer" , request.headers.get('referer'))

    return utils.showSuccess(request , "Successfully added" , referer)

def update(request):
    charuid = request.POST.get('id')
    post = request.POST.copy()
    old = Picture.objects.get(pk = charuid)
    data = {
        'id': charuid,
        'title': utils.input(request,'title', old.title),
        'image': utils.input(request,'image',old.image),
        'url': utils.input(request,'url',old.url),

    }



    model = Picture(**data)
    model.save(force_update = True)

    referer = utils.input(request , "referer" , request.headers.get('referer'))
    return utils.showSuccess(request , "Modified successfully" , referer)



