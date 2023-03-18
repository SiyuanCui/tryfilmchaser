import os
import uuid

import numpy as np
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from . import utils, models as commonModels
from urllib.parse import urljoin


def index(request):
    from .fit import CF_svd
    cf = CF_svd(k=1, r=3)
    movieslist = []
    if utils.checkLogin(request):

        # Get the content browsed by the current user
        user = commonModels.find(
            "SELECT moviesid FROM history WHERE visitor='%s' ORDER BY id desc limit %s" % (
                utils.session(request, "username"), 1,))

        # Get all users
        yonghuList = commonModels.select("SELECT * FROM users")
        data = []
        limit = 20
        for user in yonghuList:
            # Get the content browsed by the current user
            lists = commonModels.select(
                "SELECT moviesid FROM history WHERE visitor='%s' ORDER BY id desc limit %s" % (
                    user['username'], limit,))
            result = []
            for v in lists:
                result.append(int(v['moviesid']))

            if len(result):
                if len(result) != limit:
                    for i in range(limit - len(result)):
                        result.append(0)
                data.append(result)

        if len(data):
            # Give training factors to users
            result = cf.fit(np.array(data))
            ids = []
            for v in result:
                if len(v):
                    for c in v:
                        ids.append(str(c))
            # Get recommended content
            movieslist = commonModels.select("SELECT * FROM %s WHERE id in(%s) ORDER BY field(id , %s) LIMIT 4" % (
                'movies', ",".join(ids), ",".join(ids),))

        else:
            # No recommended content Get content recommendations randomly
            movieslist = commonModels.select("SELECT * FROM movies ORDER BY rand() limit 4")

    # The content is insufficient to supplement the content
    if len(movieslist) < 4:
        cs = commonModels.select("SELECT * FROM movies ORDER BY rand() limit %s" % (4 - len(movieslist)), )
        for c in cs:
            movieslist.append(c)

    print(movieslist)

    return render(request, 'index.html', locals())


def sh(request):
    tablename = utils.input(request, "tablename", "")
    yuan = utils.input(request, "yuan", "")
    id = int(utils.input(request, "id", 0))

    if yuan == "否" or yuan == "":
        sql = "UPDATE %s SET issh='是' WHERE id='%s' " % (tablename, id,)
    else:
        sql = "UPDATE %s SET issh='否' WHERE id='%s' " % (tablename, id,)

    commonModels.execute(sql)

    return utils.showSuccess(request, "Audit succeeded" if yuan == '否' or not yuan else 'Approval canceled')


# System login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        user_type = request.POST.get('user_type')

        if "a" in request.GET:
            pagerandom = request.POST.get('pagerandom')
            captcha = request.session["captchaCode"]
            if not pagerandom:
                return utils.showError(request, "Please fill in the verification code")
            if pagerandom != captcha:
                return utils.showError(request, "Verification code error")

        if not username:
            return utils.showError(request, "Please fill in the account number")
        if not password:
            return utils.showError(request, "Please fill in the password")
        if not user_type:
            return utils.showError(request, "Please select the corresponding role")
        qs = None
        if user_type == 'Admin':
            from admins.models import Admins

            qs = Admins.objects.filter(username=username, password=password)
        if user_type == 'User':
            from users.models import Users

            qs = Users.objects.filter(username=username, password=password)

        if qs is None:
            return utils.showError(request, 'No related roles found')
        list = qs.values()

        if not list:
            return utils.showError(request, "Account or password error")

        user = list[0]
        request.session['user_type'] = user_type
        request.session['login'] = user_type
        request.session['username'] = username

        for key, value in user.items():
            request.session[key] = str(value)

        if 'referer' in request.POST:
            referer = request.POST.get('referer')
        else:
            referer = '/main'

        return utils.showSuccess(request, "Login succeeded", referer)
    else:
        # Access page
        return render(request, 'login.html', locals())


# Generate verification code
# https://www.cnblogs.com/3one/p/8461306.html  Refer to this website to make a function
def captcha(request):
    img, strs = utils.create_validate_code(size=(120, 30))
    request.session["captchaCode"] = strs
    from io import BytesIO
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    print("Verification code value：%s" % (strs,))

    return HttpResponse(data, content_type='image/png')


# Log out
def logout(request):
    request.session.flush()
    return redirect('/')


# Management background main page
def main(request):
    return render(request, 'main.html')


def adminsy(request):
    return render(request, 'sy.html', locals())


def createUUID():
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))))
    return ''.join(uid.split('-'))


# Create your views here.
def get_path_format_vars():
    return {
        "year": datetime.datetime.now().strftime("%Y"),
        "month": datetime.datetime.now().strftime("%m"),
        "day": datetime.datetime.now().strftime("%d"),
        "date": datetime.datetime.now().strftime("%Y%m%d"),
        "time": datetime.datetime.now().strftime("%H%M%S"),
        "datetime": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "uuid": createUUID(),
        "rnd": random.randrange(1000, 9999)
    }


def upload(request):
    """Get the backend URL address of the ueditor"""
    return render(request, 'upload/upload.html', )


def get_output_path(request, path_format_var):
    # Get the path of the output file
    OutputPathFormat = ("%(uuid)s%(rnd)s.%(extname)s" % path_format_var).replace("\\", "/")
    # Explode OutputPathFormat
    OutputPath, OutputFile = os.path.split(OutputPathFormat)
    OutputPath = os.path.join(settings.MEDIA_ROOT, OutputPath)
    # If the OutputFile is empty, the inputPathFormat passed in does not contain a file name, so the default file name needs to be used

    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)
    return (OutputPathFormat, OutputPath, OutputFile)


def UploadFile(request):
    """Upload file"""
    if not request.method == "POST":
        return HttpResponse(json.dumps({'state': 'ERROR'}), content_type="application/javascript")

    state = "SUCCESS"
    # Upload file

    UploadFieldName = 'upfile'

    # Get the uploaded file
    file = request.FILES.get(UploadFieldName, None)
    if file is None:
        return HttpResponse(json.dumps({'state': 'ERROR'}), content_type="application/javascript")
    upload_file_name = file.name
    upload_file_size = file.size

    # Get the original name of the uploaded file
    upload_original_name, upload_original_ext = os.path.splitext(
        upload_file_name)

    path_format_var = get_path_format_vars()
    path_format_var.update({
        "basename": upload_original_name,
        "extname": upload_original_ext[1:],
        "filename": upload_file_name,
    })
    # Get the path of the output file
    OutputPathFormat, OutputPath, OutputFile = get_output_path(request, path_format_var)

    # Write file after all detection
    if state == "SUCCESS":
        state = save_upload_file(
            file, os.path.join(OutputPath, OutputFile))

    # Return data
    return_info = {
        # Saved file name
        'url': urljoin(settings.MEDIA_URL, OutputPathFormat),
        'original': upload_file_name,  # original filename
        'type': upload_original_ext,
        'state': state,
        # Upload status, SUCCESS will be returned when successful, and any other value will be returned to the picture upload box as is
        'size': upload_file_size
    }
    return HttpResponse(json.dumps(return_info, ensure_ascii=False), content_type="application/javascript")


def save_upload_file(PostFile, FilePath):
    try:
        f = open(FilePath, 'wb')
        for chunk in PostFile.chunks():
            f.write(chunk)
    except Exception as E:
        f.close()
        return u"Write file error: {}".format(E.message)
    f.close()
    return u"SUCCESS"


# Check whether the data of the table in the database exists
def checkno(request):
    table = utils.input(request, 'table')
    col = utils.input(request, "col")
    checktype = utils.input(request, "checktype")
    value = utils.input(request, col)

    sql = "SELECT COUNT(*) count,'1' as id FROM %s WHERE %s='%s' " % (table, col, value,)

    if checktype == "update":
        id = utils.input(request, "id")
        sql += " AND id!=%s " % (id,)

    d = commonModels.find(sql)
    count = d['count']

    if count:
        return HttpResponse('false')
    else:
        return HttpResponse('true')


def mod(request):
    if request.method == 'POST':
        oldPwd = request.POST.get("oldPwd", "")
        newPwd = request.POST.get("newPwd", "")
        newPwd2 = request.POST.get("newPwd2", "")

        if not all([oldPwd, newPwd2, newPwd]):
            return utils.showError(request,
                                   "Please fill in the original password or new password or confirm the password")

        if newPwd != newPwd2:
            return utils.showError(request, "Wrong password entered twice")
        user_type = request.session["login"]
        username = request.session["username"]
        qs = None
        passwordfield = ''

        if user_type == 'admin':
            from admins.models import Admins

            qs = Admins.objects.filter(username=username, password=oldPwd)
            passwordfield = 'pwd'
        if user_type == 'user':
            from users.models import Users

            qs = Users.objects.filter(username=username, password=oldPwd)
            passwordfield = 'password'

        if qs is None:
            return utils.showError(request, "No such user")

        values = qs.all()
        if not len(values):
            return utils.showError(request, "The original password is incorrect")

        user = values[0]
        setattr(user, passwordfield, newPwd)
        user.save()
        return utils.showSuccess(request, "Password modified successfully", "/common/mod/")
    else:
        return render(request, 'mod.html')


def selectUpdateSearch(request):
    import json
    where = json.loads(request.POST.get('where'))
    table = request.POST.get('table')
    className = utils.parseName(table)
    fromName = table + '.models'
    model = utils.imports(fromName, className)
    if model is None:
        return HttpResponse('Error', status=500)

    qs = model.objects
    pagesize = 50

    for key, value in where.items():
        if key == 'limit':
            pagesize = int(value)
        else:
            if isinstance(value, str):
                filters = {}
                filters[key] = value
                qs = qs.filter(**filters)
            else:
                exp = value[0]
                val = value[1]
                if exp == '>':
                    exp = 'gt'
                elif exp == '>=':
                    exp = 'gte'
                elif exp == '<':
                    exp = 'lt'
                elif exp == '<=':
                    exp = 'lte'
                elif exp == 'like':
                    exp = 'icontains'
                elif exp == 'not in':
                    zd = {}
                    k = "pk" if key == 'id' else key
                    zd["%s__%s" % (k, "in")] = val.split(",") if isinstance(val, str) else val
                    qs = qs.exclude(**zd)
                    continue
                elif exp == 'in':
                    exp = 'in'
                    val = val.split(",") if isinstance(val, str) else val
                else:
                    exp = ''

                if exp == '':
                    zd = {}
                    zd[key] = val
                    qs = qs.filter(**zd)
                else:
                    field = key + '__' + exp
                    zd = {}
                    zd[field] = val
                    qs = qs.filter(**zd)
    pass
    lists = list(qs.values()[0:pagesize])

    print(lists)
    return HttpResponse(json.dumps(lists, cls=utils.DecimalEncoder))
