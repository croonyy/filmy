"""filmy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf.urls import include
from django.views.generic.base import RedirectView
from django.conf import settings
# from django.views.generic import TemplateView
from filmy import views as filmy_views

from rest_framework.documentation import include_docs_urls

import logging

logger = logging.getLogger('ud_logger')

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'', RedirectView.as_view(url=r'/rbac/swagger/')),
    re_path('^static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path('^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    path(r'icon_vendor/', filmy_views.icon_vendors, name='icon_vendors'),
    path(r'icon_admin/', filmy_views.icon_admin, name='icon_admin'),

    re_path(r'^favicon\.ico', RedirectView.as_view(url=r'static/img/logo/favicon.ico')),

    path('drf_docs/', include_docs_urls(title='API文档', description="description"),
         name='drf_docs'),
    # 如果存在权限的问题，加上 authentication_classes=[], permission_classes=[] 约束
    # 例如: include_docs_urls(title='API', authentication_classes=[],
    # permission_classes=[])

]

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    urlpatterns += [path('admin/', admin.site.urls, name='admin')]

if 'filmy.UdAdmin.UdAdminConfig' in settings.INSTALLED_APPS:
    urlpatterns += [path('admin/', admin.site.urls, name='admin')]

if 'filmy.ud_admin_site.UdAdmin.UdAdminConfig' in settings.INSTALLED_APPS:
    urlpatterns += [path('admin/', admin.site.urls, name='admin')]

# 如果 UD_APPS 添加了app 则自动添加app路由
if not settings.DJANGO_DEFAULT:
    for ud_app_name in settings.UD_APPS:  # 前面6个app是系统自带的
        print("installed ud app:[{}] namespace:[{}]".format(ud_app_name, ud_app_name))
        url_pre = '{}/'.format(ud_app_name)
        urls = include((ud_app_name + '.urls', ud_app_name), namespace=ud_app_name)
        urlpatterns += [path(url_pre, urls)]
else:
    for ud_app_name in settings.UD_APPS:  # 前面6个app是系统自带的
        print("ud app:[{}] not migrated,namespace:[{}]".format(ud_app_name, ud_app_name))

print('*' * 80)
# logger.info(msg='*' * 80)
