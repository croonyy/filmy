from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from rbac import models
from django.urls import reverse
from django.views.generic import View
# import json
# from rbac.util.user_perms import perm_init

import json
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth import login as admin_login, logout as admin_logout
import pprint
pp = pprint.PrettyPrinter(indent=2)

# from util import timer

# from django.utils.module_loading import import_string


# import logging
# logger = logging.getLogger()

# from django.contrib.auth.views import auth_login

# rbac_user = get_user_model()

# @method_decorator(login_required, name='dispatch')  # 未登录重定向到login页面
class ud_login(View):
    def get(self, request):
        next_url = request.GET.get('next', '')
        print(next_url)
        return render(request, 'rbac/login.html')

    # @timer
    def post(self, request, **kwargs):
        print(f"get_full_path:{request.get_full_path()}")
        # print(dir(request))

        # print(json.dumps({k: str(request[k]) for k in dir(request)}, indent=4))
        pp.pprint({k: str(getattr(request, k)) for k in dir(request)})
        # print(json.dumps({k: str(getattr(request, k)) for k in dir(request)}, indent=4))
        next_url = request.GET.get('next', '')
        print(f"next_url:{next_url}")
        # print(request.path)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = request.user
        try:
            user = authenticate(request, username=username, password=password)
            # user.is_active = 1
            if user:
                # print(user.__dict__)
                if hasattr(user, 'ldap_user'):
                    print('ldap authenticate:{}'.format(user))
                    print(user.ldap_user._user_dn)
                    user.is_staff = 1
                    if "ou=商业智能部,ou=三诺健康,ou=营销中心,ou=三诺生物传感股份有限公司,ou=三诺生物传感股份有限公司,dc=sinocare,dc=com" in user.ldap_user._user_dn:
                        user.roles.add(7, 8)
                        user.groups.add(1)
                    user.save()
                else:
                    print('models authenticate:'.format(user))
            print("authenticate finished,user:{}".format(user))
            # print(user)

        except Exception as e:
            print(str(e))
            return render(request, 'rbac/login.html', {'login_error': str(e), 'msg': '登录错误:{}'.format(str(e))})
        if user and user.is_active:
            print(user.is_active)
            print(f'login:{user}')
            # perm_init(request, user)  # 设置权限列表函数 SimpleLazyObject(lambda: get_user_perms(request, user))
            admin_login(request, user, backend=None)  # 先要设置permissions_list，再调用admin的login(因为这个函数会重定向)
            if next_url == "":
                return redirect(reverse("rbac:index"))
            else:
                return HttpResponseRedirect(next_url)
        else:
            return render(request, 'rbac/login.html',
                          {'login_error': '用户名或密码错误，请重新登录。', 'msg': '用户名或密码错误，请重新登录。'})


class ud_logout(View):
    def get(self, request):
        # if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        # return redirect(reverse("rbac:index"))
        request.session.flush()  # 删除perm_list
        # 或者使用下面的方法
        # del request.session['is_login']
        # del request.session['user_id']
        # del request.session['user_name']
        admin_logout(request)  # 调用admin的logout
        return redirect('/')


class register(View):
    def get(self, request):
        # print(reverse("pet:register"))
        # get的时候不能用redirect,循环引用了，不知道要返回哪个html模板给客户端
        # return redirect(reverse("pet:register"))
        return render(request, "pet/user_center/register.html")

    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)
        print(username, password, re_password)
        if not username and password and re_password:  # 确保用户名和密码都不为空
            return render(request, 'pet/user_center/register.html',
                          {'register_error': '信息填写不完整', 'msg': '信息填写不完整！'})
        if models.CustomerLogin.objects.filter(login_name=username):
            return render(request, 'pet/user_center/register.html',
                          {'register_error': '用户名已经存在！', 'msg': '用户已经存在，请更换用户名重新注册！'})
        if password != re_password:
            return render(request, 'pet/user_center/register.html',
                          {'register_error': '两次密码不一致', 'msg': '两次密码输入不一致！'})
        else:
            try:
                # 保存用户
                user = models.CustomerLogin()
                user.login_name = username
                user.password = password
                user.user_stats = 1
                user.save()
                print(user.customer_id)
                # 设置登录状态
                request.session['is_login'] = True
                request.session['login_name'] = user.login_name
                request.session['customer_id'] = user.customer_id
                request.session['head_img_url'] = "/media/img/head_img/default.jpg"
                return redirect(reverse("pet:index"))
            except Exception as e:
                return render(request, 'pet/user_center/register.html',
                              {'register_error': '内部错误', 'msg': str(e)})
