# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.log import logger
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import simplejson
from django.db.models.query_utils import Q
from assets.models import asset,log

@login_required
def assets_asset(request):
    path = request.path.split('/')[1]
    return render_to_response('assets/assets_asset.html',{'user':request.user.username,
                                                           'path1':'assets',
                                                           'path2':path,
                                                           'page_name1':u'资产管理',
                                                           'page_name2':u'资产出入库'})

@login_required
def assets_asset_data(request):
        sEcho =  request.POST.get('sEcho') #标志，直接返回
        iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
        iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
        iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
        sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
        sSearch = request.POST.get('sSearch')#高级搜索

        aaData = []
        sort = ['name','assets_type','assets_code','comment','add_time','id']

        if  sSortDir_0 == 'asc':
            if sSearch == '':
                result_data = asset.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = asset.objects.all().count()
            else:
                result_data = asset.objects.filter(Q(name__contains=sSearch) | \
                                                   Q(assets_type__contains=sSearch) | \
                                                   Q(assets_code__contains=sSearch) | \
                                                   Q(comment__contains=sSearch) | \
                                                   Q(id__contains=sSearch)) \
                                                .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = asset.objects.filter(Q(name__contains=sSearch) | \
                                                     Q(assets_type__contains=sSearch) | \
                                                     Q(assets_code__contains=sSearch) | \
                                                     Q(comment__contains=sSearch) | \
                                                     Q(id__contains=sSearch)).count()
        else:
            if sSearch == '':
                result_data = asset.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = asset.objects.all().count()
            else:
                result_data = asset.objects.filter(Q(name__contains=sSearch) | \
                                                   Q(assets_type__contains=sSearch) | \
                                                   Q(assets_code__contains=sSearch) | \
                                                   Q(comment__contains=sSearch) | \
                                                   Q(id__contains=sSearch)) \
                                                .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = asset.objects.filter(Q(name__contains=sSearch) | \
                                                     Q(assets_type__contains=sSearch) | \
                                                     Q(assets_code__contains=sSearch) | \
                                                     Q(comment__contains=sSearch) | \
                                                     Q(id__contains=sSearch)).count()
        for i in  result_data:
            aaData.append({
                           '0':i.name,
                           '1':i.assets_type,
                           '2':i.assets_code,
                           '3':i.comment,
                           '4':str(i.add_time).split('+')[0],
                           '5':i.id
                          })
        result = {'sEcho':sEcho,
                   'iTotalRecords':iTotalRecords,
                   'iTotalDisplayRecords':iTotalRecords,
                   'aaData':aaData
        }
        return HttpResponse(simplejson.dumps(result),content_type="application/json")

def assets_asset_save(request):
    _id = request.POST.get('id')
    assets_type = request.POST.get('assets_type')
    comment = request.POST.get('comment')
    assets_code = request.POST.get('assets_code')
    name = request.POST.get('name')
    comment_info = u'%s|%s|%s 入库' % (name,assets_type,assets_code)

    if _id =='':
        orm = asset(name=name,assets_type=assets_type,assets_code=assets_code,comment=comment)
        orm_log = log(comment=comment_info)
    else:
        orm = asset.objects.get(id=int(_id))
        orm.name = name
        orm.assets_type = assets_type
        orm.assets_code = assets_code
        orm.comment = comment

    try:
        orm_log.save()
        orm.save()
        return HttpResponse(simplejson.dumps({'code':0,'msg':u'保存成功'}),content_type="application/json")
    except Exception,e:
        logger.error(e,comment)
        return HttpResponse(simplejson.dumps({'code':1,'msg':u'保存失败'}),content_type="application/json")
