import re
import json
import traceback
import pprint
import time

from django.utils.functional import SimpleLazyObject
from django.conf import settings
from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.db.models import signals
from django.core.exceptions import FieldDoesNotExist
from django.utils.deprecation import MiddlewareMixin
# from django.http import HttpResponseRedirect
# from django.contrib.auth.models import AnonymousUser
# from django import conf
# from rbac.util.user_perms import get_user_perms, check_user_perm
from rbac.util.tools_ud import curry
from rbac.models import RequestRecord

pp = pprint.PrettyPrinter(indent=2)


# from django.contrib.auth import AnonymousUser


class PermissionMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        # 查看当前的请求路径
        current_path = request.path
        print("请求路径:{}  方法:{}".format(current_path, request.method))
        # print("request.user.lastlogin", request.user.last_login)
        print(f'request.user:{request.user}')
        # print(request.user.__dict__)
        # if isinstance(request.user, AnonymousUser):
        #     return None

        # 超级管理员放行
        # print(request.user)
        if request.user.is_superuser:
            print('superuser管理员放行')
            return None  # 放行

        # 1 放行白名单
        white_list = ['/$', '/rbac/', "/rbac/login/.*", "/rbac/logout/.*", "/admin/.*", "/media.*", '/rbac/test/.*',
                      '/favicon.ico', '/static/.*', '/login/', '/logout/',
                      '/report/common/get_embed_info/', '/report/get_wx_code/', '/report/common/get_ss_dashboard/',
                      '/sino/gitlab_webhook/', ]
        # '/favicon.ico', '/static/.*', '/login/', '/logout/', '/sino/url_test', '/sino/query_data/']
        for reg in white_list:
            # if re.search(reg, current_path):
            if re.match(reg, current_path):
                # print('白名单放行')
                print("白名单 match succ:[{}]=[{}] 放行".format(reg, current_path))
                return None  # 放行

        # 2 判断是否登录(非白名单都需要登录)
        # # if not request.session.get("user_id"):
        # if not request.user.is_authenticated:
        #     print('未登录重定向到登录页面:{}'.format(settings.LOGIN_URL))
        #     return redirect(settings.LOGIN_URL)

        # 3 权限校验
        # 获取当前用户的权限列表
        permission_list = request.session.get("perm_list")

        # 每次请求都做权限更新太耗资源，舍弃这个方式，
        # 好处是不需要重新登录就能刷新权限
        # try:
        #     print('尝试获取perms_obj')
        #     permission_list = request.perms_obj
        # except Exception as e:
        #     permission_list = []
        #     print('获取perms_obj失败 设置permission_list=[] 空列表')
        #     print(str(e))

        # url匹配
        if permission_list:
            # print('permission_list = request.perms_obj，权限校验')
            print(f'权限校验:[{current_path}] in session["perm_list"]')
            for parm_dict in permission_list:
                if parm_dict['type'] == 'menu_perm':  # 排除菜单权限
                    continue
                if check_user_perm(parm_dict['url'], current_path):
                    print("url match succ:[{}]=[{}]".format(parm_dict['url'], current_path))
                    return None

        # 匹配失败返回页面或者json
        print("url match failed.")
        if request.method == 'GET':
            return render(request, "rbac/perm_denied.html", {'current_path': current_path})
        elif request.method == 'POST':
            return JsonResponse({"status": 0, "msg": "permission denied"})
        else:
            return JsonResponse({"status": 0, "msg": "request.method[{}] not defined".format(request.method)})

        # return HttpResponse("url：[{}]，您没有访问权限！<br>您有权访问的url列表：<br>{}"
        #                     .format(current_path, str('<br>'.join([str(i) for i in permission_list]))))
        # else:
        # print(current_path)
        # return render(request, "rbac/permdenied.html")
        # return HttpResponse("url：[{}]，您没有任何访问权限！".format(current_path))


class AdminAuthenticationRedirect(MiddlewareMixin):
    def process_request(self, request):
        current_path = request.path
        if re.match("^/admin/login/.*$", current_path):
            # login_url = reverse("rbac:login")
            login_url = '/'
            print(f"admin登录重定向：{login_url}")
            # return redirect(settings.LOGIN_URL)
            return redirect(login_url)

        # if re.match("^/admin/logout/.*$", current_path):
        #     # logout_url = reverse("rbac:logout")
        #     logout_url = reverse("rbac:logout")
        #     print(f"admin登出重定向:{logout_url}")
        #     return redirect(logout_url)


# 不能中间件设置权限列表，消耗数据库资源，应该在登录函数里面设置权限对象，这样登录一次才更新一次权限，
# 而不是每次访问都更新权限列表
class PermlistMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        # print('中间间设置request.perms_obj')
        request.perms_obj = SimpleLazyObject(lambda: get_user_perms(request, user))

        # request.perms_obj = SimpleLazyObject(get_user_perms(request, user))

        # if request.path == settings.LOGIN_URL and request.method == 'POST':
        #     print(f'POST请求:{settings.LOGIN_URL} 请求完执行权限设置。')
        #     # 因为是登录后设置 所以要lazy加载一个函数，登录后才运行这个函数
        #     request.perms_obj = SimpleLazyObject(lambda: get_user_perms(request, user))
        #     # request.perms_obj = SimpleLazyObject(get_user_perms(request, user))
        #     # print(str(request.perms_obj))
        # else:
        #     # print('该请求不是登录')
        #     pass


# class MiddlewareMixin(object):
#     def __init__(self, get_response=None):
#         self.get_response = get_response
#         super(MiddlewareMixin, self).__init__()
#
#     def __call__(self, request):
#         response = None
#         if hasattr(self, 'process_request'):
#             response = self.process_request(request)
#         if not response:
#             response = self.get_response(request)
#         if hasattr(self, 'process_response'):
#             response = self.process_response(request, response)
#         return response


class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # 添加响应头

        # 允许你的域名来获取我的数据
        response['Access-Control-Allow-Origin'] = "*"

        # 允许你携带Content-Type请求头
        # response['Access-Control-Allow-Headers'] = "Content-Type"

        # 允许你发送DELETE,PUT
        # response['Access-Control-Allow-Methods'] = "DELETE,PUT"

        # 预检请求 -- 登陆的跨域
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            # 需要什么类型的请求头就在后面直接添加，不能加*
            response['Access-Control-Allow-Methods'] = 'PUT,DELETE,POST,GET'

        return response


class WhoDidMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            if hasattr(request, 'user') and request.user.is_authenticated:
                user = request.user
            else:
                user = None

            mark_whodid = curry(self.mark_whodid, user)
            signals.pre_save.connect(mark_whodid, dispatch_uid=(self.__class__, request,), weak=False)

    def process_response(self, request, response):
        if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            signals.pre_save.disconnect(dispatch_uid=(self.__class__, request,))
        return response

    def mark_whodid(self, user, sender, **kwargs):  # sender必须显示传入回调函数
        # create_by_field, update_by_field = conf.settings.CREATE_BY_FIELD, conf.settings.UPDATE_BY_FIELD
        create_by_field, update_by_field = "create_by", "update_by"
        obj = kwargs['instance']  # kwargs有参数signal-信号实例，instance-发出信号的实例，raw，using，update_fields
        try:
            obj._meta.get_field(create_by_field)
            print()
        except FieldDoesNotExist:
            pass
        else:
            if not getattr(obj, create_by_field):
                setattr(obj, create_by_field, user)

        try:
            obj._meta.get_field(update_by_field)
        except FieldDoesNotExist:
            pass
        else:
            setattr(obj, update_by_field, user)


class RequestRecordMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # pass
        print(f"request.path:{request.path}")
        # setattr(request, 'test_aa', 'test_aa')
        pass

    def process_response(self, request, response):
        try:
            # print(dir(request))
            # print(dir(response))
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META.get('HTTP_X_FORWARDED_FOR')
            else:
                ip = request.META.get('REMOTE_ADDR')
            dict_c = {
                # "get_args": str(dict(request.GET)),
                # "post_args": str(dict(request.POST)),
                "get_args": json.dumps(request.GET, ensure_ascii=False),
                "post_args": json.dumps(request.POST, ensure_ascii=False),
                "user": request.user.username,
                "content_params": json.dumps(request.content_params, ensure_ascii=False),
                "content_type": request.content_type,
                "encoding": request.encoding,
                "headers": request.headers.__str__(),
                # "headers": json.dumps(request.headers, ensure_ascii=False),
                "method": request.method,
                "app_name": request.resolver_match.app_name,
                "app_names": json.dumps(request.resolver_match.app_names, ensure_ascii=False),
                "args": request.resolver_match.args,
                "kwargs": json.dumps(request.resolver_match.kwargs, ensure_ascii=False),
                "namespace": request.resolver_match.namespace,
                "namespaces": request.resolver_match.namespaces,
                "route": request.resolver_match.route,
                "url_name": request.resolver_match.url_name,
                "view_name": request.resolver_match.view_name,
                "scheme": request.scheme,
                "ip_from": ip,
                "res_charset": response.charset,
                "res_closed": response.closed,
                "res_cookies": response.cookies.__str__(),
                "res_reason_phrase": response.reason_phrase,
                "res_status_code": response.status_code,
                "res_streaming": response.streaming,
            }
            request_record = RequestRecord(**dict_c)
            request_record.save()
            # print(json.dumps({k: str(v) for k, v in dict_c.items()}, indent=4))
            # pp.pprint({k: str(getattr(request, k)) for k in dir(request)})
            # print(json.dumps({k: str(v) for k, v in dir(request)}, indent=4))
            print("save request_record succ.")
        except Exception as e:
            print(traceback.format_exc())
            pass
        return response


if __name__ == '__main__':
    # print(get_current_user())
    pass
