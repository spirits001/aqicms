# encoding: utf-8
"""
@author: 代码厨子
@license: (C) Copyright 2020.
@contact: hofeng@aqifun.com
@software: Python 3
@time: 2020-12-09 18:18
"""

import datetime
from .models import Report


# 更新统计数据
def create_report():
    today = datetime.datetime.now().date()
    data = {
        "views": 1
    }
    try:
        report = Report.objects.get(date=today)
        report.views += 1
        report.save()
    except:
        Report.objects.create(**data)
