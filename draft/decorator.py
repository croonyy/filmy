from django.http import JsonResponse
from functools import wraps
import re
from django.shortcuts import render
from rbac.util.user_perms import check_user_perm
from rbac.util.url_white_list import white_list
from rbac.util.user_perms import get_user_perms

def rbac_check(func):
    """
    decorator for check rbac perms
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # if 'request' not in kwargs.keys():
        if not args[0]:
            return JsonResponse({"status": 0, "msg": "request obj not exists."})
            # print(kwargs['request'])
        # request = kwargs['kwargs']
        request = args[0]
        current_path = request.path
        print("请求路径:{}  方法:{}".format(request.path, request.method))
        # 1 超级管理员放行
        # print(request.user)
        if request.user.is_superuser:
            print('superuser管理员放行')
            return func(*args, **kwargs)
            # return None  # 放行

        # 2 放行白名单
        # '/favicon.ico', '/static/.*', '/login/', '/logout/', '/sino/url_test', '/sino/query_data/']
        for reg in white_list:
            # if re.search(reg, current_path):
            if re.match(reg, current_path):
                # print('白名单放行')
                print("白名单 match succ:[{}] 放行".format(reg))
                return func(*args, **kwargs)
                # return None  # 放行

        # 2 判断是否登录(非白名单都需要登录)
        # # if not request.session.get("user_id"):
        # if not request.user.is_authenticated:
        #     print('未登录重定向到登录页面:{}'.format(settings.LOGIN_URL))
        #     return redirect(settings.LOGIN_URL)

        # 3 权限校验
        # 每次请求都做权限更新太耗资源，舍弃这个方式，
        # 好处是不需要重新登录就能刷新权限
        # try:
        #     print('尝试获取perms_obj')
        #     permission_list = request.perms_obj
        # except Exception as e:
        #     permission_list = []
        #     print('获取perms_obj失败 设置permission_list=[] 空列表')
        #     print(str(e))

        # 获取当前用户的权限列表
        # permission_list = request.session.get("perm_list")
        permission_list = get_user_perms(request.user)

        # url匹配
        if permission_list:
            # print('permission_list = request.perms_obj，权限校验')
            print(f'权限校验:[{current_path}] in session["perm_list"]')
            for parm_dict in permission_list:
                if parm_dict['type'] == 'menu_perm':  # 排除菜单权限
                    continue
                if check_user_perm(parm_dict['url'], current_path):
                    print("url match succ:[{}]".format(parm_dict['url']))
                    return func(*args, **kwargs)
                    # return None #匹配成功放行
        # 匹配失败返回页面或者json
        print("权限检查不放行")
        if request.method == 'GET':
            return render(request, "rbac/perm_denied.html", {'current_path': current_path})
        elif request.method == 'POST':
            return JsonResponse({"status": 0, "msg": "permission denied"})
        else:
            return JsonResponse({"status": 0, "msg": "request.method[{}] not defined".format(request.method)})
        # result = func(*args, **kwargs)
        # return func(*args, **kwargs)
    return wrapper
