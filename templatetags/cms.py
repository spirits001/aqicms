# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2019.
@contact: hofeng@yongdaoyun.com
@software: Python 3
@file: cms.py
@time: 2019-10-04 20:55
@desc:
"""
import datetime
from django import template
from django.conf import settings
from django.forms.models import model_to_dict
from app_article.models import Article, Category
from app_ad.models import Ads

# 创建模板库的实例
register = template.Library()


# 获得URL
@register.filter
def get_link(obj):
    if not obj:
        return ''
    if obj.redirect:
        return obj.redirect
    dict_obj = model_to_dict(obj)
    if 'supplement' in dict_obj:
        supplement = ''
        if obj.supplement:
            supplement = obj.supplement
        return "/c/%s.html%s" % (obj.hash_id, supplement)
    if 'category' in dict_obj:
        return "/a/%s.html" % obj.hash_id
    else:
        return "/i/%s.html" % obj.hash_id


# 获取顶级分类
@register.filter
def top_category(obj):
    return obj.filter(father__isnull=True)


# 获得下属子分类
@register.filter
def sub_category(obj, father):
    return obj.filter(father__hash_id=father)


# 逐级获得分类
@register.filter
def category_list(hash_id):
    res = []
    loop = True
    try:
        category = Category.objects.get(hash_id=hash_id)
        res.insert(0, category)
        while loop:
            if category.father:
                res.insert(0, category.father)
                category = category.father
            else:
                loop = False
        return res
    except BaseException:
        return res


# 获取某分类下所有文章
@register.filter
def get_article(hash_id, order_by='-id'):
    return Article.objects.filter(category__hash_id=hash_id, isHidden=False).order_by('sort', order_by)


# 获取某分类下子分类所有文章
@register.filter
def get_sub_article(hash_id):
    return Article.objects.filter(category__father__hash_id=hash_id, isHidden=False).order_by('category__sort', 'category_id', 'sort', '-id')


@register.filter
def get_tag_article(tags, order_by='-id'):
    return Article.objects.filter(tag__title__in=tags.split(',')).order_by(order_by)


# 获取有图文章
@register.filter
def get_img_article(obj):
    return obj.exclude(img='')


# 获取广告列表
@register.filter
def get_ads(gid):
    now = datetime.datetime.now()
    return Ads.objects.filter(group_id=int(gid), start_time__lte=now, end_time__gte=now)


# 获取文章或单页
@register.filter
def get_detail(obj, hash_id):
    try:
        return obj.get(hash_id=hash_id)
    except BaseException:
        return None


# 获取图片路径
@register.filter
def static_image(obj):
    if obj:
        return settings.ALI_MEDIA_URL + str(obj)
    return settings.EMPTY_IMAGE


@register.filter
def next_article(aid):
    article = Article.objects.filter(id__gt=aid).first()
    if article:
        return get_link(article, 'a')
    return ''


@register.filter
def before_article(aid):
    article = Article.objects.filter(id__lt=aid).first()
    if article:
        return get_link(article, 'a')
    return ''


@register.filter
def nearby(article, direction):
    if direction == 'before':
        return Article.objects.filter(category=article.category, id__lt=article.id).order_by('-id').first()
    if direction == 'after':
        return Article.objects.filter(category=article.category, id__gt=article.id).order_by('id').first()
    return None


@register.filter
def get_static(static, sid):
    try:
        static_row = static.get(id=sid)
        return static_row.title
    except:
        return ''
