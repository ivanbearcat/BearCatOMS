# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.log import logger
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import simplejson,re
from django.db.models.query_utils import Q
from audit.models import log

@login_required
def audit_log(request):
    path = request.path.split('/')[1]
    return render_to_response('audit/audit_log.html',{'user':request.user.username,
                                                           'path1':'audit',
                                                           'path2':path,
                                                           'page_name1':u'运维审计',
                                                           'page_name2':u'操作日志'})

@login_required
def audit_log_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['source_ip','username','command','time','id']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = log.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = log.objects.all().count()
        else:
            result_data = log.objects.filter(Q(source_ip__contains=sSearch) | \
                                            Q(username__contains=sSearch) | \
                                            Q(command__contains=sSearch) | \
                                            Q(time__contains=sSearch) | \
                                               Q(id__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = log.objects.filter(Q(source_ip__contains=sSearch) | \
                                            Q(username__contains=sSearch) | \
                                            Q(command__contains=sSearch) | \
                                            Q(time__contains=sSearch) | \
                                                 Q(id__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = log.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = log.objects.all().count()
        else:
            result_data = log.objects.filter(Q(source_ip__contains=sSearch) | \
                                            Q(username__contains=sSearch) | \
                                            Q(command__contains=sSearch) | \
                                            Q(time__contains=sSearch) | \
                                               Q(id__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = log.objects.filter(Q(source_ip__contains=sSearch) | \
                                            Q(username__contains=sSearch) | \
                                            Q(command__contains=sSearch) | \
                                            Q(time__contains=sSearch) | \
                                                 Q(id__contains=sSearch)).count()
    for i in  result_data:
        aaData.append({
                       '0':i.source_ip,
                       '1':i.username,
                       '2':i.command,
                       '3':i.time,
                       '4':i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(simplejson.dumps(result),content_type="application/json")

def audit_get_data(request):
    ip = request.POST.get('ip')
    username = request.POST.get('username')
    command = request.POST.get ('command')
    time = request.POST.get ('time')
    try:
        log.objects.create(source_ip=ip,username=username,command=command,time=time)
        return HttpResponse('success')
    except Exception,e:
        logger.error(e)
        return HttpResponse('error')