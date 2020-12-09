# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@time: 2020-12-09 18:18
"""

import xadmin
# from xadmin.plugins.auth import PermissionModelMultipleChoiceField, UserCreationForm, UserChangeForm
# from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
from .models import *


class GroupAdmin(object):
    model_icon = 'fa fa-book'


class AdsAdmin(object):
    list_display = ["title", "group", "image", "start_time", "end_time", "redirect", "sort", "num"]
    search_fields = ["title", ]
    list_filter = ["group", "start_time", "end_time"]
    list_editable = ["sort"]
    readonly_fields = ["num"]
    model_icon = 'fa fa-flag'


class TagAdmin(object):
    model_icon = 'fa fa-tags'


xadmin.site.register(Group, GroupAdmin)
xadmin.site.register(Ads, AdsAdmin)
xadmin.site.register(Tag, TagAdmin)
