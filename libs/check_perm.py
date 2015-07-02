#!/usr/bin/env python
#coding:utf-8
from user_manage.models import perm
from django.shortcuts import render_to_response


def check_permission(perm_name,username):
    flag = 0
    orm = perm.objects.get(username=username)
    for i in orm.web_perm.split(','):
        if perm_name == i or u'所有权限' == i:
            flag += 1
    return flag



