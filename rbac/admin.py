from django.contrib import admin
from rbac.ud_admin.model_admin import UdModelAdmin
import sys
import inspect
from rbac import models as md
from django.contrib.auth.models import Group, Permission as AuthPermission
from rbac.util.ud_user_admin import GroupAdmin, UserAdmin
from rbac.util.admin_tools import PrettyJSONWidget
from django.db.models import JSONField

from django import forms
from rbac.ud_admin import widgets as ud_widgets
from rbac.ud_admin import fields as ud_fields
from rbac.ud_admin.forms import TestForm, GenerateUdModelForm

from filmy import views as filmy_view
from rbac.util import admin_tools as at

admin.site.site_title = "系统后台"
admin.site.site_header = "后台管理"
admin.site.index_title = "后台主页"

# class UserInfoInline(admin.StackedInline): # TabularInline
#     extra = 0
#     model = models.UserInfo

# Now register the new UserAdmin...
# admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
#
models_to_register = ['Permission', 'ViewObject', 'PermissionView',
                      'Role', 'PermissionViewRole',
                      # 'Test',
                      'MenuTest',
                      ]

# 批量创建管理类
reg_dict = {}

for model_name, model in inspect.getmembers(sys.modules[md.__name__], inspect.isclass):
    # print(model_name)
    if model_name in models_to_register:
        admin_class = type(model_name + 'ModelAdmin', (UdModelAdmin,), {})
        display_list = [i.name for i in model._meta.fields]
        admin_class.Media = type('Media', (), {})
        admin_class.Media.css = {'all': ['admin_ud/admin_ud.css', ]}
        # admin_class.actions = ['make_copy', 'custom_button']
        if hasattr(model, 'exe_btn'):
            display_list.append('exe_btn')
            admin_class.Media.js = ['admin_ud/admin_ud.js', ]
            admin_class.Media.css['all'].append('admin_ud/fixed_last_colum.css')
        admin_class.list_display = display_list
        admin_class.list_per_page = 25
        reg_dict[model_name] = {'model': model, 'admin': admin_class}
    else:
        continue

#
# for k, v in reg_dict.items():
#     print(k, v)

# 管理类的模型个性化
if 'Permission' in reg_dict.keys():
    obj = reg_dict['Permission']['admin']
    # obj.list_filter = ['type']
    obj.search_fields = ['name']

if 'ViewObject' in reg_dict.keys():
    obj = reg_dict['ViewObject']['admin']
    obj.list_filter = ['permissionview__permission__name']
    # obj.list_filter = ['type']
    obj.search_fields = ['name', 'extra']
    # obj.formfield_overrides = {JSONField: {'widget': PrettyJSONWidget}}  # 放最后一行才生效

if 'PermissionView' in reg_dict.keys():
    obj = reg_dict['PermissionView']['admin']
    obj.list_filter = ['permission']
    # obj.autocomplete_fields = ['permission', ]
    obj.search_fields = ['name', 'permission__name', 'view_object__name', 'extra']
    obj.autocomplete_fields = ['permission', 'view_object', 'parent']
    # obj.search_fields = ['parent__permission__name']
    # obj.formfield_overrides = {JSONField: {'widget': PrettyJSONWidget}}

if 'Role' in reg_dict.keys():
    obj = reg_dict['Role']['admin']
    obj.filter_horizontal = ('permission_views',)

if 'Test' in reg_dict.keys():
    model_ = reg_dict['Test']['model']
    obj = reg_dict['Test']['admin']
    # obj.changelist_view = ud_changelist_view

model_str = 'MenuTest'
if model_str in reg_dict.keys():
    obj = reg_dict[model_str]['admin']
    obj.changelist_view = at.menu_view(filmy_view.icon_vendors)

# if 'User' in reg_dict.keys():
#     obj = reg_dict['User']['admin']
#     obj.filter_horizontal = ('permissions',)

# 注册模型
for k, v in reg_dict.items():
    admin.site.register(v['model'], v['admin'])

# 单独注册用户模型 GroupAdmin, UserAdmin
spec_admin = {
    "User": {"model": md.User, "admin": UserAdmin},
    "Group": {"model": Group, "admin": GroupAdmin},
    # "AuthPermission":
    #     {"model": AuthPermission,
    #      "admin": type("AuthPermission" + 'ModelAdmin', (admin.ModelAdmin,), {})},
}

# Group源码django.contrib.auth.admin已经注册过了，如需替换，则需先注销
admin.site.unregister(Group)
# 如果修改app_label,意味着这个模型的所属app发生变更，会导致migrations发生变更
# Group._meta.app_label = 'rbac'
Group._meta.verbose_name = "分组"
Group._meta.verbose_name_plural = "分组"

# 注册模型
for k, v in spec_admin.items():
    admin_class = v['admin']
    admin_class.Media = type('Media', (), {})
    admin_class.Media.css = {'all': ['admin_ud/admin_ud.css', ]}
    admin_class.Media.css['all'].append('admin_ud/fixed_last_colum.css')
    admin.site.register(v['model'], v['admin'])

# Group._meta.app_label = group_label
