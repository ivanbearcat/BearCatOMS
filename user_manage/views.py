#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.log import logger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import simplejson,re
from user_manage.models import perm
from operation.models import server_group_list
from django.db.models.query_utils import Q
from BearCatOMS.settings import BASE_DIR

@login_required
def chpasswd(request):
    path = request.path.split('/')[1]
    return render_to_response('user_manage/chpasswd.html',{'user':request.user.username,
                                                           'path1':'user_manage',
                                                           'path2':path,
                                                           'page_name1':u'用户管理',
                                                           'page_name2':u'修改密码',})

@login_required
def post_chpasswd(request):
    password_current = request.POST.get('password_current')
    password_new = request.POST.get('password_new')
    password_new_again = request.POST.get('password_new_again')
    print password_current,password_new,password_new_again
    user = User.objects.get(username=request.user.username)
    if not user.check_password(password_current):
        code = 1
        msg = u'当前密码错误'
    elif password_new == '' or password_new_again == '':
        code = 2
        msg = u'新密码不能为空'
    elif not password_new == password_new_again:
        code = 3
        msg = u'新密码不一致'
    else:
        try:
            user.set_password(password_new)
            user.save()
            code = 0
            msg = u'密码修改成功'
        except Exception,e:
            print e
            code = 4
            msg = u'密码修改失败'
    return HttpResponse(simplejson.dumps({'code':code,'msg':msg}),content_type="application/json")

@login_required
def user_perm(request):
    if not request.user.is_superuser:
        return render_to_response('public/no_passing.html')
    path = request.path.split('/')[1]
    return render_to_response('user_manage/user_perm.html',{'user':request.user.username,
                                                           'path1':'user_manage',
                                                           'path2':path,
                                                           'page_name1':u'用户管理',
                                                           'page_name2':u'用户权限管理',})

@login_required
def user_perm_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['username','name',None,None,'server_groups','server_password_expire']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = perm.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = perm.objects.all().count()
        else:
            result_data = perm.objects.filter(Q(username__contains=sSearch) | \
                                               Q(name__contains=sSearch) | \
                                               Q(web_perm__contains=sSearch) | \
                                               Q(server_groups__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = perm.objects.filter(Q(username__contains=sSearch) | \
                                                 Q(name__contains=sSearch) | \
                                                 Q(web_perm__contains=sSearch) | \
                                                 Q(server_groups__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = perm.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = perm.objects.all().count()
        else:
            result_data = perm.objects.filter(Q(username__contains=sSearch) | \
                                               Q(name__contains=sSearch) | \
                                               Q(web_perm__contains=sSearch) | \
                                               Q(server_groups__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = perm.objects.filter(Q(username__contains=sSearch) | \
                                                 Q(name__contains=sSearch) | \
                                                 Q(web_perm__contains=sSearch) | \
                                                 Q(server_groups__contains=sSearch)).count()

    for i in  result_data:
        aaData.append({
                       '0':i.username,
                       '1':i.name,
                       '2':i.web_perm,
                       '3':i.server_password,
                       '4':str(i.server_password_expire),
                       '5':i.server_groups,
                       '6':i.id,
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(simplejson.dumps(result),content_type="application/json")

@login_required
def user_perm_dropdown(request):
    _id = request.POST.get('id')
    result = {}
    result['username_list'] = []
    result['username_edit'] = []
    result['web_perm_list'] = []
    result['web_perm_edit'] = []
    result['server_groups_list'] = []
    result['server_groups_edit'] = []
    if not _id == None:
        orm = server_group_list.objects.get(id=_id)
        for i in orm.members_server.split(','):
            orm_server = server_list.objects.get(server_name=i)
            result['edit'].append({'text':i,'id':orm_server.id})
    orm_User = User.objects.all()
    for i in orm_User:
        result['username_list'].append({'text':i.username,'id':i.id})
    sidebar_list = []
    sidebar_list2 = []
    count = 0
    with open(BASE_DIR + '/templates/public/sidebar.html') as f:
        line = f.readline()
        while line:
            data = re.search(r'/.*/',line)
            if data:
                sidebar_list.append(data.group().replace('/',''))
            line = f.readline()
    for i in sidebar_list:
        if  i != 'main' or i != 'user_perm':
            sidebar_list2.append(i)
    for i in sidebar_list2:
        result['web_perm_list'].append({'text':i,'id':count})
        count += 1
    orm_server_group = server_group_list.objects.all()
    for i in orm_server_group:
        result['server_groups_list'].append({'text':i.server_group_name,'id':i.id})
    return HttpResponse(simplejson.dumps(result),content_type="application/json")