# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.log import logger
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def main(request):
    return render_to_response('public/index.html')