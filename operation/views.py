# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.log import logger
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import simplejson,re,os,datetime
from django.db.models.query_utils import Q
from operation.models import upload_files
from django import forms

@login_required
def upload(request):
    path = request.path.split('/')[1]
    return render_to_response('operation/upload.html',{'user':request.user.username,
                                                           'path1':'operation',
                                                           'path2':path,
                                                           'page_name1':u'运维操作',
                                                           'page_name2':u'文件上传'})

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

def handle_uploaded_file(request,f):
    file_name = ''
    try:
        path = 'uploads/'
        file_name = path + f.name
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.isfile(file_name):
            time = datetime.datetime.now().strftime('%Y%m%d%H%M')
            os.rename(file_name,file_name + '_' + time)
            orm = upload_files.objects.get(file_name=f.name)
            orm.file_name = f.name + '_' + time
            orm.save()
        file = open(file_name, 'wb+')
        for chunk in f.chunks():
            file.write(chunk)
        file.close()
        file_size = os.path.getsize(file_name)
        upload_files.objects.create(file_name=f.name,file_size=file_size,upload_user=request.user.username)
    except Exception, e:
        print e
        logger.error(e)
    return file_name

def get_upload(request):
    file = request.FILES.get('file')
    if not file == None:
        handle_uploaded_file(request,file)
    return HttpResponse(simplejson.dumps({'msg': "上传成功", "code": 0}),content_type="application/json")

def upload_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['file_name','file_size','upload_time','upload_user']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = upload_files.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = upload_files.objects.all().count()
        else:
            result_data = upload_files.objects.filter(Q(file_name__contains=sSearch) | \
                                               Q(file_size__contains=sSearch) | \
                                               Q(upload_user__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = upload_files.objects.filter(Q(file_name__contains=sSearch) | \
                                                 Q(file_size__contains=sSearch) | \
                                                 Q(upload_user__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = upload_files.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = upload_files.objects.all().count()
        else:
            result_data = upload_files.objects.filter(Q(file_name__contains=sSearch) | \
                                               Q(file_size__contains=sSearch) | \
                                               Q(upload_user__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = upload_files.objects.filter(Q(file_name__contains=sSearch) | \
                                                 Q(file_size__contains=sSearch) | \
                                                 Q(upload_user__contains=sSearch)).count()

    for i in  result_data:
        if len(str(i.file_size)) >= 4 and len(str(i.file_size)) < 7:
            file_size = i.file_size / 1024.0
            file_size = re.search(r'\d+\.\d\d',str(file_size))
            file_size = file_size.group() + 'K'
        elif len(str(i.file_size)) >= 7 and len(str(i.file_size)) < 10:
            file_size = i.file_size / 1024.0 / 1024.0
            file_size = re.search(r'\d+\.\d\d',str(file_size))
            file_size = file_size.group() + 'M'
        elif len(str(i.file_size)) >= 10:
            file_size = i.file_size / 1024.0 / 1024.0 / 1024.0
            file_size = re.search(r'\d+\.\d\d',str(file_size))
            file_size = file_size.group() + 'G'
        aaData.append({
                       '0':i.file_name,
                       '1':file_size,
                       '2':str(i.upload_time).split('+')[0],
                       '3':i.upload_user,
                       '4':i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(simplejson.dumps(result),content_type="application/json")

def upload_del(request):
    _id = request.POST.get('id')
    orm = upload_files.objects.get(id=_id)
    try:
        os.remove('uploads/' + orm.file_name)
        orm.delete()
        return HttpResponse(simplejson.dumps({'code':0,'msg':u'删除成功'}),content_type="application/json")
    except Exception,e:
        logger.error(e)
        return HttpResponse(simplejson.dumps({'code':1,'msg':str(e)}),content_type="application/json")