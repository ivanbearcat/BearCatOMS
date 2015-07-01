# -*- coding: utf-8 -*-
from django.db import models

class perm(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, blank=False)
    name = models.CharField(verbose_name='姓名',max_length=32)
    web_perm = models.CharField(verbose_name='网页权限',max_length=256)
    server_password = models.CharField(verbose_name='服务器密码',max_length=64)
    server_groups = models.CharField(verbose_name='服务器组',max_length=64)
    server_password_expire = models.DateField(verbose_name='服务器密码过期时间')