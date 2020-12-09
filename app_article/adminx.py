# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@time: 2020-12-09 18:18
"""

import xadmin
from xadmin.layout import Main, Fieldset, Row, Side
from .models import *


class CategoryAdmin(object):
    list_display = ["title", "father", "template", "image", "isNew", "isDelete", "isHidden", "sort", "hash_id"]
    search_fields = ["title", "hash_id"]
    list_filter = ["father", "isNew", "isDelete", "isHidden"]
    list_editable = ["isNew", "isDelete", "isHidden", "sort"]
    readonly_fields = ["hash_id"]
    model_icon = 'fa fa-folder'

    form_layout = (
        Main(
            Fieldset(None,
                     'hash_id', **{"style": "display:None"}
                     ),
            Fieldset('必填',
                     'title',
                     Row('template', 'article_template')
                     ),
            Fieldset('SEO',
                     Row('description', 'keywords')
                     ),
            Fieldset('选填',
                     Row('father', 'redirect'),
                     'img'
                     ),
        ),
        Side(
            Fieldset('辅助',
                     "isNew", "isDelete", "isHidden", "sort", "supplement"
                     ),
        )
    )


class ArticleAdmin(object):
    list_display = ["title", "category", "tag", "image", "add_time", "author", "isHidden", "sort", "num", "hash_id"]
    search_fields = ["title", "hash_id"]
    list_filter = ["category", "isHidden", "add_time", "author", "tag"]
    list_editable = ["sort"]
    readonly_fields = ["hash_id", "num"]
    style_fields = {'body': 'ueditor'}
    model_icon = 'fa fa-envelope-open'

    form_layout = (
        Fieldset(None,
                 'hash_id', 'num', **{"style": "display:None"}
                 ),
        Fieldset('基础内容',
                 Row('title', 'sub_title'),
                 Row('category', 'author'),
                 Row('show_time', 'template'),
                 "body"
                 ),
        Fieldset('SEO',
                 Row('description', 'keywords')
                 ),
        Fieldset('选填',
                 Row('come', 'redirect'),
                 Row("img", "tag"),
                 Row("isHidden", "sort"),
                 )
    )

    class ArticleImagesInline(object):
        model = ArticleImages
        extra = 1

    inlines = [ArticleImagesInline]


class IntroAdmin(object):
    list_display = ["title", "template", "image", "add_time", "isHidden", "sort", "num", "hash_id"]
    search_fields = ["title", "hash_id"]
    list_filter = ["isHidden", "add_time"]
    list_editable = ["sort"]
    readonly_fields = ["hash_id", "num"]
    style_fields = {'body': 'ueditor'}
    model_icon = 'fa fa-calendar'

    form_layout = (
        Fieldset(None,
                 'hash_id', 'num', **{"style": "display:None"}
                 ),
        Fieldset('基础内容',
                 Row('title', 'sub_title'),
                 Row('template', 'sort'),
                 "body"
                 ),
        Fieldset('SEO',
                 Row('description', 'keywords')
                 ),
        Fieldset('选填',
                 Row('redirect', 'img'), "isHidden"
                 )
    )

    class IntroImagesInline(object):
        model = IntroImages
        extra = 1

    inlines = [IntroImagesInline]


xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Intro, IntroAdmin)
