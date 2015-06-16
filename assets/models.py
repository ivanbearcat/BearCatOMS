# -*- coding: utf-8 -*-
from django.db import models

class asset(models.Model):
    name = models.CharField(verbose_name='资产名', max_length=30, blank=False)
    assets_type = models.CharField(verbose_name='资产型号', max_length=30)
    assets_code = models.CharField(verbose_name='资产编号', max_length=30)
    comment = models.CharField(verbose_name='备注', max_length=256)
    add_time = models.DateTimeField(verbose_name='入库时间', auto_now_add=True)

class user(models.Model):
    name = models.CharField(verbose_name='员工名', max_length=30, blank=False)
    department = models.CharField(verbose_name='部门', max_length=30, blank=False)
    device = models.ForeignKey(asset)
    comment = models.CharField(verbose_name='备注', max_length=256)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

class log(models.Model):
    comment = models.CharField(verbose_name='备注', max_length=256)
    add_time = models.DateTimeField(verbose_name='记录时间', auto_now_add=True)


