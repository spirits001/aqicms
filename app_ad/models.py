# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@time: 2020-12-09 18:18
"""
from django.db import models
from django.utils.html import format_html
from django.conf import settings


# Create your models here.
class Group(models.Model):
    """
    广告组
    """
    title = models.CharField(max_length=50, unique=True, verbose_name='标题', help_text='标题')

    class Meta:
        verbose_name = '广告组管理'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.title


class Ads(models.Model):
    """
    广告
    """
    group = models.ForeignKey(to='Group', on_delete=models.PROTECT, related_name='rn_ads_group', verbose_name='所属广告组', help_text='所属广告组')
    title = models.CharField(max_length=50, verbose_name='标题', help_text='标题')
    start_time = models.DateTimeField(verbose_name='开始时间', help_text='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间', help_text='结束时间')
    redirect = models.CharField(max_length=255, verbose_name='跳转地址', help_text='跳转地址')
    img = models.ImageField(null=True, blank=True, verbose_name='广告图片', help_text='广告图片')
    sort = models.IntegerField(default=1000, verbose_name='排序ID', help_text='数字越小，排名越靠前')
    num = models.IntegerField(default=0, verbose_name='阅读量', help_text='阅读量')

    def image(self):
        if self.img:
            return format_html("<img src='{}{}' height='100px' />", settings.ALI_MEDIA_URL, self.img)
        else:
            return '无图片'

    class Meta:
        verbose_name = '广告管理'
        verbose_name_plural = verbose_name
        ordering = ['sort', 'id']

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    标签管理
    """
    title = models.CharField(max_length=50, unique=True, verbose_name='Tag', help_text='Tag', default='')

    class Meta:
        verbose_name = 'Tag管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
