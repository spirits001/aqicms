# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@time: 2020-12-09 18:18
"""
from django.http import HttpResponseRedirect
from django.http import Http404
from app_users.api import create_report
from .models import *


# Create your views here.

def ad(request, ad_id):
    try:
        ads = Ads.objects.get(id=int(ad_id))
        ads.num += 1
        ads.save()
        create_report()
        return HttpResponseRedirect(ads.redirect)
    except BaseException:
        raise Http404()
