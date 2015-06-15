#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.log import logger
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import simplejson

def chpasswd(request):
    path = request.path.split('/')[1]
    return render_to_response('user_manage/chpasswd.html',{'user':request.user.username,
                                                           'path1':'user_manage',
                                                           'path2':path,
                                                           'page_name1':u'用户管理',
                                                           'page_name2':u'修改密码',})


def post_chpasswd(request):
    password_current = request.POST.get('password_current')
    password_new = request.POST.get('password_new')
    password_new_again = request.POST.get('password_new_again')
    print password_current,password_new,password_new_again
    user = User.objects.get(username=request.user.username)
    if not user.check_password(password_current):
        code = 1
        msg = u'当前密码错误'
    elif not password_new == password_new_again:
        code = 2
        msg = u'新密码不一致'
    else:
        try:
            user.set_password(password=password_new)
            user.save
            code = 0
            msg = u'密码修改成功'
        except Exception,e:
            print e
            code = 3
            msg = u'密码修改失败'
    return HttpResponse(simplejson.dumps({'code':code,'msg':msg}),content_type="application/json")