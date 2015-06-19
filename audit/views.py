# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.log import logger
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import simplejson
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

def audit_get_data(request):
    ip = request.POST.get('ip')
    username = request.POST.get('username')
    command = request.POST.get ('command')
    print ip,username,command
    log.objects.create(source_ip=ip,username=username,command=command)
    return HttpResponse('OK')