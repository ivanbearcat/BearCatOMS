# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.log import logger
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def nagios(request):
    path = request.path.split('/')[1]
    return render_to_response('monitor/nagios.html',{'user':request.user.username,
                                                     'path1':'monitor',
                                                     'path2':path,
                                                     'page_name1':u'监控',
                                                     'page_name2':'nagios'})
def zabbix(request):
    path = request.path.split('/')[1]
    return render_to_response('monitor/zabbix.html',{'user':request.user.username,
                                                     'path1':'monitor',
                                                     'path2':path,
                                                     'page_name1':u'监控',
                                                     'page_name2':'zabbix'})
