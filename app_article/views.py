# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@time: 2020-12-09 18:18
"""
from django.http import Http404
from django.shortcuts import render
from django.db.models import Q
from utils.core import get_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_users.api import create_report
from app_ad.models import Group
from app_users.models import Static
from .models import *

PAGE_NUM = 20


def category_top(category):
    loop = True
    while loop:
        if category.father:
            category = category.father
        else:
            loop = False
    return category


# Create your views here.
def cms_index(request):
    """
    整站首页
    :param request:
    :return:
    """
    create_report()
    data = {
        'site_name': settings.SITENAME,
        'category': Category.objects.filter(isDelete=False, isHidden=False),
        'intro': Intro.objects.filter(isHidden=False),
        'article': Article.objects.all(),
        'group': Group.objects.all(),
        'static': Static.objects.all()
    }
    return render(request, settings.TEMPLATE_NAME + '/cms_index.html', data)


def cms_list(request, hash_id):
    """
    新闻列表页
    :param request:
    :param hash_id:
    :return:
    """
    create_report()
    category_all = Category.objects.filter(isDelete=False, isHidden=False)
    try:
        category = category_all.get(hash_id=get_id(hash_id))
        data = {
            'category_top': category_top(category),
            'site_name': settings.SITENAME,
            'category_list': category,
            'category_sub': category_all.filter(father=category),
            'category': category_all,
            'intro': Intro.objects.filter(isHidden=False),
            'article': Article.objects.all(),
            'static': Static.objects.all()
        }
    except BaseException:
        raise Http404('喔豁~~木有！')
    data["articles"] = Article.objects.filter(category=category, isHidden=False).order_by('sort', '-id')
    paginator = Paginator(data["articles"], PAGE_NUM)
    page = request.GET.get('page')
    try:
        data["articles"] = paginator.page(page)
    except PageNotAnInteger:
        data["articles"] = paginator.page(1)
    except EmptyPage:
        data["articles"] = paginator.page(paginator.num_pages)
    template = category.template
    if data['category_sub'].count() and template == 'cms_list.html':
        template = 'cms_channel.html'
    return render(request, settings.TEMPLATE_NAME + '/' + template, data)


def cms_detail(request, hash_id):
    """
    新闻最终页
    :param request:
    :param hash_id:
    :return:
    """
    try:
        article = Article.objects.get(hash_id=get_id(hash_id))
        article.num += 1
        create_report()
        data = {
            'category_top': category_top(article.category),
            'site_name': settings.SITENAME,
            "article": article,
            'album': ArticleImages.objects.filter(article=article),
            'category': Category.objects.filter(isDelete=False, isHidden=False),
            'intro': Intro.objects.filter(isHidden=False),
            'static': Static.objects.all()
        }
        article.save()
        return render(request, settings.TEMPLATE_NAME + '/' + article.template, data)
    except BaseException:
        raise Http404('喔豁~~木有！')


def cms_intro(request, hash_id):
    """
    文章单页
    :param request:
    :param hash_id:
    :return:
    """
    try:
        intro = Intro.objects.get(hash_id=get_id(hash_id))
        intro.num += 1
        create_report()
        data = {
            'site_name': settings.SITENAME,
            "intro": intro,
            'category': Category.objects.filter(isDelete=False, isHidden=False),
            'static': Static.objects.all(),
            'album': IntroImages.objects.filter(intro=intro),
        }
        intro.save()
        return render(request, settings.TEMPLATE_NAME + '/' + intro.template, data)
    except BaseException:
        raise Http404('喔豁~~木有！')


def cms_search(request):
    """
    文章搜索页面
    :param request:
    :return:
    """
    create_report()
    keywords = request.GET["keywords"]
    list_keys = keywords.split(' ')
    list_articles = Article.objects.filter(isHidden=False)
    articles = list_articles.filter(Q(title__icontains=list_keys[0]) | Q(description__icontains=list_keys[0]))
    for item in list_keys:
        articles = articles | list_articles.filter(Q(title__icontains=item) | Q(description__icontains=item))
    put_articles = articles.order_by('sort', '-id').distinct()
    data = {
        'category': Category.objects.filter(isDelete=False, isHidden=False),
        'intro': Intro.objects.filter(isHidden=False),
        'article': list_articles,
        'static': Static.objects.all(),
        "keywords": keywords,
        "articles": put_articles,
        "count": put_articles.count()
    }
    paginator = Paginator(data["articles"], PAGE_NUM)
    page = request.GET.get('page')
    try:
        data["articles"] = paginator.page(page)
    except PageNotAnInteger:
        data["articles"] = paginator.page(1)
    except EmptyPage:
        data["articles"] = paginator.page(paginator.num_pages)
    return render(request, settings.TEMPLATE_NAME + '/cms_search.html', data)
