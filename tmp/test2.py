#coding:utf-8
import re
from BearCatOMS.settings import BASE_DIR

def check_permission(arg):
    def _check_permission(func):
        def __check_permission():
            flag = 0
            print arg
            # orm = perm.objects.get(username=request.user.username)
            # for i in orm.web_perm.split(','):
            #     if u'修改密码' == i or u'所有权限' == i:
            #         flag += 1
            # if flag < 1:
            #     return render_to_response('public/no_passing.html')
            func()
        return __check_permission
    return _check_permission



@check_permission(111111)
def a():
    print 222

a()