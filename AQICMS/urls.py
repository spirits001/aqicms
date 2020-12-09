"""AQICMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.conf.urls import url
from django.views.static import serve

import xadmin

xadmin.autodiscover()

from xadmin.plugins import xversion

xversion.register_models()

from app_users.views import *
from app_article.views import *
from app_ad.views import *

urlpatterns = [
    path('', cms_index),
    path('search', cms_search),
    re_path(r'^c/([A-Za-z0-9.]+)$', cms_list),
    re_path(r'^a/([A-Za-z0-9.]+)$', cms_detail),
    re_path(r'^i/([A-Za-z0-9.]+)$', cms_intro),
    re_path(r'^ad/([0-9]+)$', ad),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    url(r'manage/', xadmin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
]
