# Generated by Django 3.1.4 on 2020-12-09 17:38

import DjangoUeditor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_ad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='标题', max_length=255, verbose_name='标题')),
                ('sub_title', models.CharField(blank=True, default='', help_text='副标题', max_length=255, null=True, verbose_name='副标题')),
                ('body', DjangoUeditor.models.UEditorField(blank=True, null=True, verbose_name='内容')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
                ('show_time', models.DateTimeField(blank=True, help_text='指定页面显示时间，留空为添加修改时间', null=True, verbose_name='显示时间')),
                ('author', models.CharField(default='本站', help_text='作者', max_length=100, verbose_name='作者')),
                ('redirect', models.CharField(blank=True, help_text='跳转地址', max_length=300, null=True, verbose_name='跳转地址')),
                ('template', models.CharField(default='cms_detail.html', help_text='模板文件名称', max_length=50, verbose_name='模板名称')),
                ('img', models.ImageField(blank=True, help_text='文章显示主图', null=True, upload_to='', verbose_name='文章主图')),
                ('sort', models.IntegerField(default=1000, help_text='数字越小，排名越靠前', verbose_name='排序ID')),
                ('hash_id', models.CharField(db_index=True, help_text='外部访问地址', max_length=20, unique=True, verbose_name='对外访问标识')),
                ('keywords', models.CharField(blank=True, default='', help_text='填写文章的关键词，用于SEO', max_length=100, null=True, verbose_name='文章关键词')),
                ('description', models.TextField(blank=True, default='', help_text='填写文章的描述，用于SEO', max_length=500, null=True, verbose_name='文章描述')),
                ('num', models.IntegerField(default=0, help_text='阅读量', verbose_name='阅读量')),
                ('come', models.CharField(blank=True, default='', help_text='来源', max_length=50, null=True, verbose_name='来源')),
                ('isHidden', models.BooleanField(default=False, help_text='选中为在文章列表中隐藏', verbose_name='隐藏文章')),
            ],
            options={
                'verbose_name': '文章管理',
                'verbose_name_plural': '文章管理',
            },
        ),
        migrations.CreateModel(
            name='Intro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='标题', max_length=255, verbose_name='标题')),
                ('sub_title', models.CharField(blank=True, default='', help_text='副标题', max_length=255, null=True, verbose_name='副标题')),
                ('body', DjangoUeditor.models.UEditorField(blank=True, null=True, verbose_name='内容')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', verbose_name='添加时间')),
                ('redirect', models.CharField(blank=True, help_text='跳转地址', max_length=300, null=True, verbose_name='跳转地址')),
                ('template', models.CharField(default='cms_intro.html', help_text='模板文件名称', max_length=50, verbose_name='模板名称')),
                ('img', models.ImageField(blank=True, help_text='文章显示主图', null=True, upload_to='', verbose_name='文章主图')),
                ('sort', models.IntegerField(default=1000, help_text='数字越小，排名越靠前', verbose_name='排序ID')),
                ('hash_id', models.CharField(db_index=True, help_text='外部访问地址', max_length=20, unique=True, verbose_name='对外访问标识')),
                ('keywords', models.CharField(blank=True, default='', help_text='填写文章的关键词，用于SEO', max_length=100, null=True, verbose_name='文章关键词')),
                ('description', models.TextField(blank=True, default='', help_text='填写文章的描述，用于SEO', max_length=500, null=True, verbose_name='文章描述')),
                ('num', models.IntegerField(default=0, help_text='阅读量', verbose_name='阅读量')),
                ('isHidden', models.BooleanField(default=False, help_text='选中为在文章列表中隐藏', verbose_name='隐藏文章')),
            ],
            options={
                'verbose_name': '单页管理',
                'verbose_name_plural': '单页管理',
                'ordering': ['sort', '-id'],
            },
        ),
        migrations.CreateModel(
            name='IntroImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='标题', max_length=255, null=True, verbose_name='标题')),
                ('img', models.ImageField(help_text='图集图片', upload_to='', verbose_name='图片')),
                ('sort', models.IntegerField(default=1000, help_text='数字越小，排名越靠前', verbose_name='排序ID')),
                ('intro', models.ForeignKey(blank=True, help_text='单页图集', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rn_intro_images_intro', to='app_article.intro', verbose_name='所属单页')),
            ],
            options={
                'verbose_name': '单页图集',
                'verbose_name_plural': '单页图集',
                'ordering': ['sort', 'id'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='文章主分类', max_length=20, verbose_name='分类名称')),
                ('keywords', models.CharField(blank=True, default='', help_text='填写分类的关键词，用于SEO', max_length=100, null=True, verbose_name='分类关键词')),
                ('description', models.TextField(blank=True, default='', help_text='填写分类的描述，用于SEO', max_length=500, null=True, verbose_name='分类描述')),
                ('hash_id', models.CharField(db_index=True, help_text='外部访问地址', max_length=20, unique=True, verbose_name='对外访问标识')),
                ('supplement', models.CharField(blank=True, default='', help_text='接在url后面的内容', max_length=100, null=True, verbose_name='额外URL')),
                ('sort', models.IntegerField(default=1000, help_text='数字越小，排名越靠前', verbose_name='排序ID')),
                ('template', models.CharField(default='cms_list.html', help_text='模板文件名称', max_length=50, verbose_name='模板名称')),
                ('article_template', models.CharField(default='cms_detail.html', help_text='下属文章模板文件名称', max_length=50, verbose_name='文章模板')),
                ('img', models.ImageField(blank=True, help_text='图片url', null=True, upload_to='', verbose_name='分类主图')),
                ('redirect', models.CharField(blank=True, help_text='跳转地址', max_length=300, null=True, verbose_name='跳转地址')),
                ('isNew', models.BooleanField(default=False, help_text='选中为弹出新窗口打开', verbose_name='弹出新窗口')),
                ('isDelete', models.BooleanField(default=False, help_text='选中为逻辑删除状态', verbose_name='逻辑删除')),
                ('isHidden', models.BooleanField(default=False, help_text='选中为在分类列表中隐藏', verbose_name='隐藏分类')),
                ('father', models.ForeignKey(blank=True, help_text='空则为跟目标', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rn_category_father', to='app_article.category', verbose_name='上级分类')),
            ],
            options={
                'verbose_name': '文章分类',
                'verbose_name_plural': '文章分类',
                'ordering': ['sort', 'id'],
            },
        ),
        migrations.CreateModel(
            name='ArticleImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='标题', max_length=255, null=True, verbose_name='标题')),
                ('img', models.ImageField(help_text='图集图片', upload_to='', verbose_name='图片')),
                ('sort', models.IntegerField(default=1000, help_text='数字越小，排名越靠前', verbose_name='排序ID')),
                ('article', models.ForeignKey(blank=True, help_text='文章图集', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rn_article_images_article', to='app_article.article', verbose_name='所属文章')),
            ],
            options={
                'verbose_name': '文章图集',
                'verbose_name_plural': '文章图集',
                'ordering': ['sort', 'id'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(help_text='所属分类', on_delete=django.db.models.deletion.PROTECT, related_name='rn_article_category', to='app_article.category', verbose_name='所属分类'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(blank=True, help_text='Tag多选', related_name='rn_article_tag', to='app_ad.Tag', verbose_name='文章Tag'),
        ),
    ]
