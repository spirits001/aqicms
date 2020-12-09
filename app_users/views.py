# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@time: 2020-12-09 18:18
"""
from django.http import HttpResponse


# Create your views here.
def index(request):
    res = "代码厨子作品"
    return HttpResponse(res)
