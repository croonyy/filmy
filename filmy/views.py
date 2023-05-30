from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
# import json

from django.contrib.auth.decorators import permission_required


# @permission_required('rbac.aaa')  # 没有权限会自动跳到登录页，如果登录了就跳到首页
def icon_vendors(request):
    print('aaaa')
    return render(request, "vendors/icofont.html")


def icon_admin(request):
    return render(request, "admin_ud/icon_admin.html")
