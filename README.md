# AQI CMS Powered By Django3

AQI CMS是连云港阿奇信息科技有限公司作品，这是一个基于Django3打造的开源CMS系统。公司经过多次版本迭代，经过多个客户项目实践，今天向全球开放源代码。旨在回报这么多年来全球开源软件给予的帮助。

在未来的时间里，每年公司将至少开源一项技术产品，公司将对客户服务的精华能力进行释放，为全球开源事业奉献一点力量。

本系统属于轻型CMS系统，适合制作企业门户，中小型资讯网站，个人网站，知识库等应用。

# 系统安装
Python 3.6+ ，数据库请符合Django3要求即可，推荐使用MySQL8.0

1，下载源码

2，建议使用虚拟环境

3，安装依赖 `pip install -r ./requirements.txt`

# 准备开始
1，修改settings.py内 SECRET_KEY 与 DATABASES

2，同步数据库，依次执行

`python ./manage.py makemigrations`

`python ./manage.py migrate`

3，创建管理员

`python ./manage.py createsuperuser`

4，运行项目

`python ./manage.py runserver`

# 后台管理
1，打开后台管理地址 `http://你的服务地址/manage`

如果创建的管理员密码无效，可以使用

`python ./manage.py changepassword 管理员用户名`
# 模板规则
整理中

# 与我联系
微信号：spirits001  代码厨子
