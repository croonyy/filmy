import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "filmy.settings")  # project_name 项目名称
django.setup()