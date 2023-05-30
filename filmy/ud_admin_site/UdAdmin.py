from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig
# from django.template.response import TemplateResponse
from django.urls import path, reverse
from filmy.views import icon_vendors
from filmy.settings import BASE_DIR
import os


class UdAdminConfig(AdminConfig):
    default_site = 'filmy.ud_admin_site.UdAdmin.UdAdmin'


# 对后台的全局修改
class UdAdmin(AdminSite):
    site_header = "后台管理"

    # 重写首页app list
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        ud_list = [
            # {
            #     "name": "测试菜单",
            #     "app_label": "ud_menu",
            #     # "app_url": "/admin/test_view",
            #     "models": [
            #         {
            #             "name": "menu_test",
            #             "object_name": "menu_test_obj",
            #             "admin_url": reverse("admin:icon_vendors"),
            #             "view_only": False,
            #         }
            #     ],
            # }
        ]
        return ud_list + app_list

    def get_urls(self):
        urls = [
            path('icon_vendors/', self.admin_view(icon_vendors),
                 name='icon_vendors')
        ]
        urls += super().get_urls()
        return urls

    # def get_urls(self):
    #     urls = [
    #         path('my_view/', self.admin_view(self.my_view), name='my_view')
    #     ]
    #     urls += super().get_urls()
    #     return urls
    #
    # def my_view(self, request):
    #     context = {
    #         **self.each_context(request),
    #         "title": "my_view",
    #     }
    #     return TemplateResponse(request, "admin/test.html", context)
