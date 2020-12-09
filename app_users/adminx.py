# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@time: 2020-12-09 18:18
"""

import xadmin
from xadmin import views
from .models import *
from django.conf import settings


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    dev = ""
    if settings.DEBUG:
        dev = "【开发版】"
    site_title = settings.SITENAME + dev
    site_footer = settings.COPYRIGHT + " " + settings.VERSION


class StaticAdmin(object):
    model_icon = 'fa fa-reorder'
    list_display = ["id", "title"]
    list_editable = ["title"]


class ReportAdmin(object):
    def has_delete_permission(self, obj=None):
        return False

    def has_add_permission(self, obj=None):
        # 禁用添加按钮
        return False

    model_icon = 'fa fa-bar-chart'
    list_display = ["date", "views"]
    readonly_fields = ["date", "views"]

    data_charts = {
        "views_count": {'title': u"日浏览量",
                        "x-field": "date",
                        "y-field": ("views",),
                        },
    }


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Static, StaticAdmin)
xadmin.site.register(Report, ReportAdmin)
