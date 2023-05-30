from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
import rbac.models as md
from util import timer
import json
# from rbac.util.user_perms import get_user_perms
# from rbac.util.decorator import rbac_check


# Create your views here.
# @rbac_check
def test(request):
    user = request.user
    if user.is_superuser:
        pass

    # if request.method == "GET":
    menu = [
        {"id": 1, "title": "菜单1", "type": "menu_perm", "parent_id": 0, "url": "a", "icon": "icofont-tags icons2",
         "perm_type": "user"},
        {"id": 2, "title": "菜单2", "type": "menu_perm", "parent_id": 0, "url": "b", "icon": None, "perm_type": "user"},
        {"id": 3, "title": "菜单11", "type": "menu_perm", "parent_id": 1, "url": "/index", "icon": "icofont-tag icons2",
         "perm_type": "user"},
        {"id": 4, "title": "菜单12", "type": "menu_perm", "parent_id": 1, "url": "ba", "icon": "icofont-tag",
         "perm_type": "user"},
        {"id": 5, "title": "菜单111", "type": "menu_perm", "parent_id": 3, "url": "/", "icon": None, "perm_type": "user"},
        {"id": 6, "title": "菜单112", "type": "menu_perm", "parent_id": 3, "url": "/", "icon": None, "perm_type": "user"},
        {"id": 7, "title": "菜单1111", "type": "menu_perm", "parent_id": 5, "url": "/", "icon": "icofont-cube",
         "perm_type": "user"},
        {"id": 8, "title": "菜单11111", "type": "menu_perm", "parent_id": 7, "url": "/", "icon": "icofont-star",
         "perm_type": "user"}]
    return render(request, "rbac/test.html", {"current_path": request.path, 'nav_data': json.dumps(menu)})
    # return render(request, "rbac/test.html", {"current_path": request.path})


# @timer
# @rbac_check
def permission_denied(request):
    current_path = request.path
    return render(request, "rbac/perm_denied.html", {'current_path': current_path})


@timer
# @rbac_check
def index(request):
    pass


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect(reverse("rbac:index"))
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect(reverse("rbac:index"))


def perm_test(request):
    return JsonResponse({'info': 'perm_test'})


def perm_test1(request):
    return JsonResponse({'info': 'perm_test1'})


def perm_test2(request):
    return JsonResponse({'info': 'perm_test2'})
