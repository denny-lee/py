from django.shortcuts import render
from .models import EngBook
from .models import Subject
from .daos import BaseDao
import re
from bson.json_util import dumps
from bson.objectid import ObjectId

from django.http import HttpResponse
from django.http import JsonResponse
# from django.template import loader
# Create your views here.


def index(request):
    subjects = BaseDao().find_all(Subject().get_coll())
    count = BaseDao().count(EngBook().get_coll())
    ctx = {
        'subjects': subjects,
        'totalCount': count
    }
    return render(request, 'polls/index.html', ctx)


def save(request):
    expr = request.POST['expr']
    trans = request.POST['trans']
    subject = request.POST['subject']
    tag = request.POST['tag']   # comma split
    example = request.POST['example']
    synonym = request.POST['synonym']   # comma split
    similar_spelling = request.POST['similar_spelling']     # comma split

    tag = trim_dedup(tag)
    synonym = trim_dedup(synonym)
    similar_spelling = trim_dedup(similar_spelling)

    obj = EngBook(expr, trans, subject, tag, example, synonym, similar_spelling)
    if not obj.checkRequired():
        return HttpResponse('error')

    coll = BaseDao().search(obj.get_coll(), {'expr': expr})

    # if len(list(coll)) > 0:
    if coll.count() > 0:
        obj.merge(coll.next())
    if BaseDao().save(obj):
        return HttpResponse("ok")

    return HttpResponse('error')


def find(request):
    oid = request.POST['id']
    if not oid:
        return JsonResponse('')
    obj = BaseDao().find_by_id(EngBook().get_coll(), ObjectId(oid))
    if not obj:
        return JsonResponse('')
    jsonstr = dumps(obj)
    return JsonResponse(jsonstr, safe=False)


def search(request):
    expr = request.POST['expr']
    if 'type' in request.POST:
        tp = request.POST['type']
    else:
        tp = None
    if tp == 'eq':
        print('fetch data if exist.')
        coll = BaseDao().search(EngBook().get_coll(), {'expr': expr})
    else:
        regx = re.compile("^"+expr, re.IGNORECASE)
        coll = BaseDao().search(EngBook().get_coll(), {'expr': {'$regex': regx}})
    jsonstr = dumps(coll)
    return JsonResponse(jsonstr, safe=False)


def remove(request):
    id = request.POST['id']
    if not id:
        return HttpResponse("error")
    if BaseDao().remove_one(EngBook().get_coll(), {'_id': ObjectId(id)}):
        return HttpResponse('ok')
    return HttpResponse('error')


def save_subject(request):
    name = request.POST['eng_name']
    if not name:
        return HttpResponse('eng_name should not be null')
    if BaseDao().save(Subject(name)):
        return HttpResponse("ok")
    return HttpResponse('error')


def search_subject(request):
    colls = BaseDao().search(Subject().get_coll(), {})
    jsonstr = dumps(colls)
    return JsonResponse(jsonstr, safe=False)


def remove_subject(request):
    id = request.POST['id']
    if not id:
        return HttpResponse("error")
    if BaseDao().remove_one(Subject().get_coll(), {'_id': ObjectId(id)}):
        return HttpResponse('ok')
    return HttpResponse('error')


def trim_dedup(str):
    if not str:
        return None
    n_arr = []
    if ',' in str:
        arr = str.split(',')
        for e in arr:
            if not e:
                continue
            if e not in n_arr:
                n_arr.append(e.strip())
        return ','.join(n_arr)
    return str
