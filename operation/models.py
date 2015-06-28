# -*- coding: utf-8 -*-
from django.db import models

class upload_files(models.Model):
    file_name = models.CharField(verbose_name='文件名', max_length=64, blank=False)
    file_size = models.IntegerField(verbose_name='文件大小', blank=False)
    upload_time = models.DateTimeField(verbose_name='上传时间', auto_now_add=True )
    upload_user = models.CharField(verbose_name='上传人', max_length=256, blank=False)

class server_list(models.Model):
    server_name = models.CharField(verbose_name='服务器名', max_length=32, blank=False)
    ip = models.IPAddressField(verbose_name='IP', blank=False)
    os = models.CharField(verbose_name='系统', max_length=32, blank=False)
    comment = models.CharField(verbose_name='备注', max_length=128)