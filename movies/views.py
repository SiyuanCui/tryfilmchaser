from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Movies
from common.utils import input
from common import utils, models as commonModels

from columns.models import Columns


# Create your views here.

def getWhere(request, qs):
    if request.GET.get("title"):
        qs = qs.filter(title__contains=request.GET.get("title"))
    if request.GET.get("column"):
        qs = qs.filter(column=request.GET.get("column"))
    if request.GET.get("director"):
        qs = qs.filter(director__contains=request.GET.get("director"))
    if request.GET.get("actor"):
        qs = qs.filter(actor__contains=request.GET.get("actor"))
    if request.GET.get("movie_start"):
        qs = qs.filter(date__lte=request.GET.get("movie_start"))

    if request.GET.get("movie_end"):
        qs = qs.filter(date__gte=request.GET.get("movie_start"))

    if request.GET.get("tags"):
        qs = qs.filter(tags__contains=request.GET.get("tags"))

    orderby = input(request, "order", "id")
    sort = input(request, "sort", "DESC").upper()
    if sort == "DESC":
        qs = qs.order_by("-" + orderby)
    else:
        qs = qs.order_by(orderby)

    return qs


# Administrator list page
def adminlist(request):
    qs = getWhere(request, Movies.objects)

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

    return render(request, "movie/admin/list.html", locals(), )


# Front list page
def index(request):
    qs = getWhere(request, Movies.objects)

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

    # context = {'list': list, 'page': list, 'paginator': paginator,
    #           'is_paginated': is_paginated,'page_range': page_range }

    return render(request, "movie/index.html", locals(), )


# Add page in the background
def adminadd(request):
    return render(request, "movie/admin/add.html", locals())


def adminupdt(request):
    id = request.GET.get("id")
    mmm = Movies.objects.get(pk=id)
    if mmm == None:
        return utils.showError(request, "No relevant data found")

    return render(request, "movie/admin/updt.html", locals())


# Background details page
def admindetail(request):
    id = request.GET.get("id")
    map = Movies.objects.get(pk=id)

    return render(request, "movie/admin/detail.html", locals())


# Front desk details page
def detail(request):
    id = request.GET.get("id")
    map = Movies.objects.get(pk=id)
    commonModels.execute("update movies set visit_count=visit_count+1 where id='%s'" % (request.GET.get("id")))

    if utils.checkLogin(request):
        commonModels.execute(
            "INSERT INTO history(moviesid,title,column,visitor,addtime) SELECT id,title,column,'%s',now() FROM movies WHERE id='%s' AND 'null'!='%s'" % (
                request.session["username"], request.GET.get("id"), request.session["username"]))

    return render(request, "movie/detail.html", locals())


def delete(request):
    ids = request.GET.getlist("id")

    for id in ids:
        map = Movies.objects.get(pk=id)

        map.delete()

    return utils.showSuccess(request, "Delete succeeded")



def insert(request):
    post = request.POST.copy()
    data = {
        'title': utils.input(request, 'title', ''),
        'column': utils.input(request, 'column', utils.input(request, 'column', 0)),
        'director': utils.input(request, 'director', ''),
        'actor': utils.input(request, 'actor', ''),
        'date': utils.input(request, 'date', ''),
        'imdb': utils.input(request, 'imdb', ''),
        'pic': utils.input(request, 'pic', ''),
        'tags': utils.input(request, 'tags', ''),
        'collection_count': utils.input(request, 'collection_count', ''),
        'visit_count': utils.input(request, 'visit_count', ''),
        'issues_count': utils.input(request, 'issues_count', ''),
        'score': utils.input(request, 'score', ''),
        'intro': utils.input(request, 'intro', ''),

    }
    if data['collection_count'] == '':
        data['collection_count'] = 0
    else:
        data['collection_count'] = int(data['collection_count'])
    if data['visit_count'] == '':
        data['visit_count'] = 0
    else:
        data['visit_count'] = int(data['visit_count'])
    if data['issues_count'] == '':
        data['issues_count'] = 0
    else:
        data['issues_count'] = int(data['issues_count'])
    if data['score'] == '':
        data['score'] = 0
    else:
        data['score'] = float(data['score'])

    model = Movies(**data)
    model.save(force_insert=True)

    referer = utils.input(request, "referer", request.headers.get('referer'))

    return utils.showSuccess(request, "Successfully added", referer)


def update(request):
    charuid = request.POST.get('id')
    post = request.POST.copy()
    old = Movies.objects.get(pk=charuid)
    data = {
        'id': charuid,
        'title': utils.input(request, 'title', old.title),
        'column': utils.input(request, 'column', utils.input(request, 'column', 0)),
        'director': utils.input(request, 'director', old.director),
        'actor': utils.input(request, 'actor', old.actor),
        'date': utils.input(request, 'date', old.date),
        'video': utils.input(request, 'video', old.video),
        'pic': utils.input(request, 'pic', old.pic),
        'tags': utils.input(request, 'tags', old.tags),
        'collection_count': utils.input(request, 'collection_count', '').strip(),
        'visit_count': utils.input(request, 'visit_count', '').strip(),
        'issues_count': utils.input(request, 'issues_count', '').strip(),
        'score': utils.input(request, 'score', '').strip(),
        'intro': utils.input(request, 'intro', old.intro),
        'addtime': old.addtime,

    }

    if data['collection_count'] == '':
        data['collection_count'] = 0
    else:
        data['collection_count'] = int(data['collection_count'])
    if data['visit_count'] == '':
        data['visit_count'] = 0
    else:
        data['visit_count'] = int(data['visit_count'])
    if data['issues_count'] == '':
        data['issues_count'] = 0
    else:
        data['issues_count'] = int(data['issues_count'])
    if data['score'] == '':
        data['score'] = 0
    else:
        data['score'] = float(data['score'])

    model = Movies(**data)
    model.save(force_update=True)

    referer = utils.input(request, "referer", request.headers.get('referer'))
    return utils.showSuccess(request, "Modified successfully", referer)
