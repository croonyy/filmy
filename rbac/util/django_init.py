# 初始化django项目配置，不然找不到django项目入口
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insight.settings")
django.setup()