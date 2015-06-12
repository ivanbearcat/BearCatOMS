#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.log import logger
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def chpasswd(request):
    path = request.path.split('/')[1]
    password_current = request.POST.get('password_current')
    password_new = request.POST.get('password_new')
    password_new_again = request.POST.get('password_new_again')
    print password_current,password_new,password_new_again

    return render_to_response('user_manage/chpasswd.html',{'user':request.user.username,
                                                     'path1':'user_manage',
                                                     'path2':path,
                                                     'page_name1':u'用户管理',
                                                     'page_name2':u'修改密码'})
