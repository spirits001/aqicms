# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@time: 2020-12-09 18:18
"""
from django.db import models


# Create your models here.

class Report(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name='报告时间', help_text='报告时间', unique=True)
    views = models.IntegerField(default=1, verbose_name='浏览量', help_text='浏览量')

    class Meta:
        verbose_name = '数据报告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.date.strftime("%Y-%m-%d"))


class Static(models.Model):
    title = models.CharField(max_length=500, verbose_name='静态内容')

    class Meta:
        verbose_name = '静态数据'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.title
