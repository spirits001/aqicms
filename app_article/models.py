# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@time: 2020-12-09 18:18
"""
import datetime
from django.db import models
from django.utils.html import format_html
from django.conf import settings
from DjangoUeditor.models import UEditorField
from utils.core import ShortenURL, rand_number, get_keywords, get_description


# Create your models here.
class Category(models.Model):
    """
    分类表
    """
    father = models.ForeignKey(to='Category', on_delete=models.PROTECT, related_name='rn_category_father', null=True, blank=True, verbose_name='上级分类', help_text='空则为跟目标')
    title = models.CharField(max_length=20, verbose_name='分类名称', help_text='文章主分类')
    keywords = models.CharField(null=True, blank=True, max_length=100, default='', verbose_name='分类关键词', help_text='填写分类的关键词，用于SEO')
    description = models.TextField(null=True, blank=True, max_length=500, default='', verbose_name='分类描述', help_text='填写分类的描述，用于SEO')
    hash_id = models.CharField(max_length=20, unique=True, verbose_name='对外访问标识', help_text='外部访问地址', db_index=True)
    supplement = models.CharField(max_length=100, verbose_name='额外URL', help_text='接在url后面的内容', null=True, blank=True, default='')
    sort = models.IntegerField(default=1000, verbose_name='排序ID', help_text='数字越小，排名越靠前')
    template = models.CharField(default='cms_list.html', max_length=50, verbose_name='模板名称', help_text='模板文件名称')
    article_template = models.CharField(default='cms_detail.html', max_length=50, verbose_name='文章模板', help_text='下属文章模板文件名称')
    img = models.ImageField(null=True, blank=True, verbose_name='分类主图', help_text='图片url')
    redirect = models.CharField(null=True, blank=True, max_length=300, verbose_name='跳转地址', help_text='跳转地址')
    isNew = models.BooleanField(default=False, verbose_name='弹出新窗口', help_text='选中为弹出新窗口打开')
    isDelete = models.BooleanField(default=False, verbose_name='逻辑删除', help_text='选中为逻辑删除状态')
    isHidden = models.BooleanField(default=False, verbose_name='隐藏分类', help_text='选中为在分类列表中隐藏')

    def save(self, *args, **kwargs):
        if not self.pk:
            sn = ShortenURL()
            self.hash_id = sn.encode(rand_number())
        elif not self.article_template == 'cms_detail.html':
            Article.objects.filter(category=self, template='cms_detail.html').update(template=self.article_template)
            category = Category.objects.filter(isDelete=False)
            for item in category:
                loop = True
                tmp = item
                while loop:
                    tmp = tmp.father
                    if tmp == self:
                        item.article_template = self.article_template
                        item.save()
                        Article.objects.filter(category=item, template='cms_detail.html').update(template=self.article_template)
                        loop = False
                    if not tmp:
                        loop = False
        super(Category, self).save(*args, **kwargs)

    def image(self):
        if self.img:
            return format_html("<img src='{}{}' height='100px' />", settings.ALI_MEDIA_URL, self.img)
        else:
            return '无图片'

    image.short_description = "分类图片"

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name
        ordering = ['sort', 'id']

    def __str__(self):
        return self.title


class Article(models.Model):
    """
    文章管理
    """
    category = models.ForeignKey(to='Category', on_delete=models.PROTECT, related_name='rn_article_category', verbose_name='所属分类', help_text='所属分类')
    title = models.CharField(max_length=255, verbose_name='标题', help_text='标题')
    sub_title = models.CharField(null=True, blank=True, default="", max_length=255, verbose_name='副标题', help_text='副标题')
    body = UEditorField(null=True, blank=True, width=1000, height=500, toolbars="besttome", imagePath="images/", filePath="files/", upload_settings={"imageMaxSize": 120400000}, settings={}, verbose_name='内容')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间', help_text='添加时间')
    show_time = models.DateTimeField(null=True, blank=True, verbose_name='显示时间', help_text='指定页面显示时间，留空为添加修改时间')
    author = models.CharField(default='本站', max_length=100, verbose_name='作者', help_text='作者')
    redirect = models.CharField(null=True, blank=True, max_length=300, verbose_name='跳转地址', help_text='跳转地址')
    template = models.CharField(default='cms_detail.html', max_length=50, verbose_name='模板名称', help_text='模板文件名称')
    img = models.ImageField(null=True, blank=True, verbose_name='文章主图', help_text='文章显示主图')
    sort = models.IntegerField(default=1000, verbose_name='排序ID', help_text='数字越小，排名越靠前')
    hash_id = models.CharField(max_length=20, unique=True, verbose_name='对外访问标识', help_text='外部访问地址', db_index=True)
    keywords = models.CharField(null=True, blank=True, max_length=100, default='', verbose_name='文章关键词', help_text='填写文章的关键词，用于SEO')
    description = models.TextField(null=True, blank=True, max_length=500, default='', verbose_name='文章描述', help_text='填写文章的描述，用于SEO')
    num = models.IntegerField(default=0, verbose_name='阅读量', help_text='阅读量')
    come = models.CharField(null=True, blank=True, default='', max_length=50, verbose_name='来源', help_text='来源')
    isHidden = models.BooleanField(default=False, verbose_name='隐藏文章', help_text='选中为在文章列表中隐藏')
    tag = models.ManyToManyField(to='app_ad.Tag', related_name='rn_article_tag', verbose_name='文章Tag', help_text='Tag多选', blank=True)

    def save(self, *args, **kwargs):
        if not self.keywords:
            self.keywords = get_keywords(self.title + self.body)
        if not self.description:
            self.description = get_description(self.body)
        if not self.pk:
            sn = ShortenURL()
            self.hash_id = sn.encode(rand_number())
            if not self.show_time:
                self.show_time = datetime.datetime.now()
        if not self.category.article_template == 'cms_detail.html' and self.template == 'cms_detail.html':
            self.template = self.category.article_template
        super(Article, self).save(*args, **kwargs)

    def image(self):
        if self.img:
            return format_html("<img src='{}{}' height='100px' />", settings.ALI_MEDIA_URL, self.img)
        else:
            return '无图片'

    image.short_description = "文章图片"

    class Meta:
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name
        # ordering = ['sort', '-id']

    def __str__(self):
        return self.title


class ArticleImages(models.Model):
    """
    文章图集
    """
    article = models.ForeignKey(to='Article', on_delete=models.PROTECT, related_name='rn_article_images_article', null=True, blank=True, verbose_name='所属文章', help_text='文章图集')
    title = models.CharField(null=True, blank=True, max_length=255, verbose_name='标题', help_text='标题')
    img = models.ImageField(verbose_name='图片', help_text='图集图片')
    sort = models.IntegerField(default=1000, verbose_name='排序ID', help_text='数字越小，排名越靠前')

    class Meta:
        verbose_name = '文章图集'
        verbose_name_plural = verbose_name
        ordering = ['sort', 'id']

    def __str__(self):
        return self.article.title


class Intro(models.Model):
    """
    单页管理
    """
    title = models.CharField(max_length=255, verbose_name='标题', help_text='标题')
    sub_title = models.CharField(null=True, blank=True, default="", max_length=255, verbose_name='副标题', help_text='副标题')
    body = UEditorField(null=True, blank=True, width=1000, height=500, toolbars="besttome", imagePath="/", filePath="/", upload_settings={"imageMaxSize": 120400000}, settings={}, verbose_name='内容')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间', help_text='添加时间')
    redirect = models.CharField(null=True, blank=True, max_length=300, verbose_name='跳转地址', help_text='跳转地址')
    template = models.CharField(default='cms_intro.html', max_length=50, verbose_name='模板名称', help_text='模板文件名称')
    img = models.ImageField(null=True, blank=True, verbose_name='文章主图', help_text='文章显示主图')
    sort = models.IntegerField(default=1000, verbose_name='排序ID', help_text='数字越小，排名越靠前')
    hash_id = models.CharField(max_length=20, unique=True, verbose_name='对外访问标识', help_text='外部访问地址', db_index=True)
    keywords = models.CharField(null=True, blank=True, max_length=100, default='', verbose_name='文章关键词', help_text='填写文章的关键词，用于SEO')
    description = models.TextField(null=True, blank=True, max_length=500, default='', verbose_name='文章描述', help_text='填写文章的描述，用于SEO')
    num = models.IntegerField(default=0, verbose_name='阅读量', help_text='阅读量')
    isHidden = models.BooleanField(default=False, verbose_name='隐藏文章', help_text='选中为在文章列表中隐藏')

    def save(self, *args, **kwargs):
        if not self.pk:
            sn = ShortenURL()
            self.hash_id = sn.encode(rand_number())
        if not self.keywords:
            self.keywords = get_keywords(self.title + self.body)
        if not self.description:
            self.description = get_description(self.body)
        super(Intro, self).save(*args, **kwargs)

    def image(self):
        if self.img:
            return format_html("<img src='{}{}' height='100px' />", settings.ALI_MEDIA_URL, self.img)
        else:
            return '无图片'

    image.short_description = "单页图片"

    class Meta:
        verbose_name = '单页管理'
        verbose_name_plural = verbose_name
        ordering = ['sort', '-id']

    def __str__(self):
        return self.title


class IntroImages(models.Model):
    """
    单页图集
    """
    intro = models.ForeignKey(to='Intro', on_delete=models.PROTECT, related_name='rn_intro_images_intro', null=True, blank=True, verbose_name='所属单页', help_text='单页图集')
    title = models.CharField(null=True, blank=True, max_length=255, verbose_name='标题', help_text='标题')
    img = models.ImageField(verbose_name='图片', help_text='图集图片')
    sort = models.IntegerField(default=1000, verbose_name='排序ID', help_text='数字越小，排名越靠前')

    class Meta:
        verbose_name = '单页图集'
        verbose_name_plural = verbose_name
        ordering = ['sort', 'id']

    def __str__(self):
        return self.intro.title
