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
def upload(request):
    path = request.path.split('/')[1]
    return render_to_response('operation/upload.html',{'user':request.user.username,
                                                           'path1':'operation',
                                                           'path2':path,
                                                           'page_name1':u'运维操作',
                                                           'page_name2':u'文件上传'})
