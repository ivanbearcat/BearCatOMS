# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.log import logger
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import simplejson,re,os,datetime,time,subprocess
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

@login_required
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

@login_required
def get_upload(request):
    file = request.FILES.get('file')
    if not file == None:
        handle_uploaded_file(request,file)
    return HttpResponse(simplejson.dumps({'msg': "上传成功", "code": 0}),content_type="application/json")

@login_required
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

@login_required
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

@login_required
def upload_upload(request):
    flag = request.POST.get('flag')
    file_name = request.POST.get('file_name')
    if int(flag) == 0:
        #开始传输
        # orm = upload_files.objects.get(file_name=file_name)
        cmdLine = []
        cmdLine.append('rsync')
        cmdLine.append('--progress')
        cmdLine.append('uploads/%s' % file_name)
        cmdLine.append('192.168.1.12:.')
        tmpFile = "tmp/upload.tmp"  #临时生成一个文件
        fpWrite = open(tmpFile,'w')
	with open('tmp/rsync_status_file.tmp','w') as f:
	    pass
        process = subprocess.Popen(cmdLine,stdout = fpWrite,stderr = subprocess.PIPE);
        while True:
            fpRead = open(tmpFile,'r')  #这里又重新创建了一个文件读取对象，不知为何，用上面的就是读不出来，改w+也不>行
            lines = fpRead.readlines()
            for line in lines:
                a = re.search(r'\d+%',line)
                if a:
                    with open('tmp/percent.tmp','a') as f:
                            f.write(a.group())
                    print a.group()
            if  process.poll() == 0:
                break;
            elif process.poll() == None:
                pass
            else:
                print 'error'
                break
            fpWrite.truncate()  #此处清空文件，等待记录下一次输出的进度
            fpRead.close()
            time.sleep(0.7)
        fpWrite.close()
	os.remove('tmp/rsync_status_file.tmp')
    #    error = process.stderr.read()
    #    if not error == None:
    #        print 'error info:%s' % error
        os.remove(tmpFile) #删除临时文件
        os.remove('tmp/percent.tmp')
        return HttpResponse(simplejson.dumps({'code':0,'msg':u'文件传输成功'}),content_type="application/json")
    elif int(flag) == 1:
        #获取百分比
	if os.path.exists('tmp/rsync_status_file.tmp'):
            process = 1
	else:
            process = 0
	if os.path.exists('tmp/percent.tmp'):
            with open('tmp/percent.tmp') as f:
                data = f.readline()
                if data:
                    last_percent = re.search(r'\d{1,2}%$',data)
                    if last_percent:
                        print last_percent.group()
                        return HttpResponse(simplejson.dumps({'code':0,'percent':last_percent.group(),'process':process}),content_type="application/json")
        else:
            return HttpResponse(simplejson.dumps({'code':0,'percent':0,'process':process}),content_type="application/json")
	    
    else:
        pass
        return HttpResponse(simplejson.dumps({'code':1,'msg':u'文件传输失败'}),content_type="application/json")
