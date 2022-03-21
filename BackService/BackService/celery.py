from __future__ import absolute_import
import os
from celery import Celery, platforms
from django.conf import settings
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BackService.settings')  # 项目的settings文件

app = Celery('BackService')  # 项目名为入参

app.config_from_object('django.conf:settings')  # 读取settings中的celery配置

# 解决时区问题,定时任务启动就循环输出
app.now = timezone.now

# celery自动发现所有django-app下面的任务tasks.py
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# app.conf.update(BROKER_HEARTBEAT=None)  # 防止自动退出  不知道有没有用
