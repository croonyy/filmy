# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from shortuuidfield import ShortUUIDField
from django.db import models
from rbac.util.ud_user import User
from rbac.ud_admin import fields as ud_fields
from rbac.util import admin_tools as at
from rbac.util import tools_ud as tu


# User = User
# max_length=50, blank=True, null=True, verbose_name='批次', help_text='监控批次分类用的tag'

# Create your models here.
class Permission(models.Model):
    name = models.CharField(max_length=200, verbose_name='权限类型', )
    extra = models.JSONField(verbose_name='Json配置', blank=True, null=True)

    exe_btn = tu.curry(at.set_model_btn, btn_list=[("edit", {}), ])

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'rbac_permission'
        app_label = 'rbac'
        verbose_name = "权限类型"
        verbose_name_plural = verbose_name


class ViewObject(models.Model):
    name = models.CharField(max_length=200, verbose_name='名称', )
    extra = models.JSONField(verbose_name='Json配置', blank=True, null=True)

    exe_btn = tu.curry(at.set_model_btn, btn_list=[("edit", {}), ])

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'rbac_view_object'
        app_label = 'rbac'
        verbose_name = "作用对象"
        verbose_name_plural = verbose_name


class PermissionView(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='名称',
                            help_text="取个名字便于权限识别，可不填")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE,
                                   verbose_name='权限类型')
    view_object = models.ForeignKey(ViewObject, on_delete=models.CASCADE,
                                    verbose_name='作用对象')
    # null = True 该权限的父权限可以为空， blank=True 添加该权限时可以不填内容。
    extra = models.JSONField(verbose_name='Json配置', blank=True, null=True)
    parent = models.ForeignKey("PermissionView",
                               on_delete=models.CASCADE, null=True,
                               blank=True, verbose_name='菜单父对象')

    exe_btn = tu.curry(at.set_model_btn, btn_list=[("edit", {}), ])

    # def __str__(self):
    #     permission_name = Permission.objects.filter(pk=self.permission_id)[0].name
    #     view_object_name = ViewObject.objects.filter(pk=self.view_object_id)[0].name
    #     return f"<PermissionView permission_name:{permission_name}---view_object_name:{view_object_name}>"

    def __str__(self):
        return f"[{self.name if self.name else '未填'}]:[{self.permission}]-[{self.view_object}]"

    class Meta:
        managed = True
        db_table = 'rbac_permission_view'
        app_label = 'rbac'
        verbose_name = "权限实例"
        verbose_name_plural = verbose_name


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name='角色名', )
    permission_views = models.ManyToManyField(to='rbac.PermissionView',
                                              blank=True, verbose_name="权限")

    exe_btn = tu.curry(at.set_model_btn, btn_list=[("edit", {}), ])

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'rbac_role'
        app_label = 'rbac'
        verbose_name = "角色"
        verbose_name_plural = verbose_name


class Test(models.Model):
    title = models.CharField(max_length=100, verbose_name='名称', )
    code = models.JSONField(max_length=1000, verbose_name='源码1', )
    code2 = models.TextField(max_length=1000, blank=True, null=True,
                             verbose_name='源码2', )

    exe_btn = tu.curry(at.set_model_btn, btn_list=[("edit", {}), ])

    # code2 = ud_admin.UdJsonField(max_length=1000, blank=True, null=True,
    #                                  verbose_name='源码2', )

    class Meta:
        managed = True
        db_table = 'rbac_test'
        app_label = 'rbac'
        verbose_name = "测试"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title


class MenuTest(models.Model):
    # pass
    class Meta:
        # db_table = 'rbac_menutest'
        app_label = 'rbac'
        managed = False
        verbose_name = "icon图标"
        verbose_name_plural = verbose_name


# class Menu(models.Model):
#     title = models.CharField(max_length=100, unique=True)
#     type = models.CharField(max_length=32, choices=(("menu_perm", "菜单权限"), ("url_perm", "路由权限")), default="url_perm")
#     parent = models.ForeignKey("Menu", on_delete=models.CASCADE, null=True,
#                                blank=True)  # null = True 该权限的父权限可以为空， blank=True 添加该权限时可以不填内容。
#     url = models.CharField(max_length=2000, blank=True, null=True)
#     icon = models.CharField(max_length=100, blank=True, null=True,
#                             help_text="""<pre>访问该页面选取图标复制名字填写：<a href='/icon' target='_blank'>点我访问图标库</a>\n""" + \
#                                       """格式：icofont-[复制的名字]</pre>""")
#
#     class Meta:
#         managed = True
#         db_table = 'rbac_menu'
#         app_label = 'rbac'
#         verbose_name = "角色"
#         verbose_name_plural = verbose_name


# class PermissionViewRole(models.Model):
#     role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
#     permission_view_id = models.ForeignKey(PermissionView, on_delete=models.CASCADE)
#
#     # def __str__(self):
#     #     role_name = Role.objects.filter(pk=self.role_id)[0].name
#     #     return f"<PermissionViewRole permission_view_id:{self.permission_view_id}---role_name:{role_name}>"
#     def __str__(self):
#         return str(self.pk)
#
#     class Meta:
#         managed = True
#         db_table = 'rbac_permission_view_role'
#         app_label = 'rbac'
#         verbose_name = "角色权限"
#         verbose_name_plural = verbose_name


# class RbacRole(models.Model):
#     name = models.CharField(max_length=100)
#     permissions = models.ManyToManyField("RbacPermission")
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         managed = True
#         db_table = 'rbac_role'
#         app_label = 'rbac'
#         verbose_name = "角色"
#         verbose_name_plural = verbose_name
#
#
# class RbacPermission(models.Model):
#     title = models.CharField(max_length=100, unique=True)
#     type = models.CharField(max_length=32, choices=(("menu_perm", "菜单权限"), ("url_perm", "路由权限")), default="url_perm")
#     parent = models.ForeignKey("RbacPermission", on_delete=models.CASCADE, null=True,
#                                blank=True)  # null = True 该权限的父权限可以为空， blank=True 添加该权限时可以不填内容。
#     url = models.CharField(max_length=2000, blank=True, null=True)
#     icon = models.CharField(max_length=100, blank=True, null=True,
#                             help_text="""<pre>访问该页面选取图标复制名字填写：<a href='/icon' target='_blank'>点我访问图标库</a>\n""" + \
#                                       """格式：icofont-[复制的名字]</pre>""")
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         managed = True
#         db_table = 'rbac_permission'
#         app_label = 'rbac'
#         verbose_name = "权限"
#         verbose_name_plural = verbose_name


class RequestRecord(models.Model):
    get_args = models.TextField(blank=True, null=True)
    post_args = models.TextField(blank=True, null=True)
    user = models.CharField(max_length=50, blank=True, null=True)
    content_params = models.TextField(blank=True, null=True)
    content_type = models.TextField(blank=True, null=True)
    encoding = models.CharField(max_length=50, blank=True, null=True)
    headers = models.TextField(blank=True, null=True)
    method = models.CharField(max_length=50, blank=True, null=True)
    app_name = models.CharField(max_length=50, blank=True, null=True)
    app_names = models.CharField(max_length=100, blank=True, null=True)
    args = models.TextField(blank=True, null=True)
    kwargs = models.TextField(blank=True, null=True)
    namespace = models.CharField(max_length=50, blank=True, null=True)
    namespaces = models.TextField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)
    url_name = models.CharField(max_length=100, blank=True, null=True)
    view_name = models.CharField(max_length=100, blank=True, null=True)
    scheme = models.CharField(max_length=50, blank=True, null=True)
    ip_from = models.CharField(max_length=50, blank=True, null=True)
    res_charset = models.CharField(max_length=50, blank=True, null=True)
    res_closed = models.BooleanField(blank=True, null=True)
    res_cookies = models.TextField(blank=True, null=True)
    res_reason_phrase = models.CharField(max_length=50, blank=True, null=True)
    res_status_code = models.IntegerField(blank=True, null=True)
    res_streaming = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    def __str__(self):
        return self.view_name

    class Meta:
        managed = True
        db_table = 'rbac_request_record'
        app_label = 'rbac'
        verbose_name = "请求记录"
        verbose_name_plural = verbose_name

# class RbacUdUserRoles(models.Model):
#     rbacuser = models.ForeignKey(RbacUser, on_delete=models.CASCADE, null=True, blank=True)
#     rbacrole = models.ForeignKey(RbacUdRole, on_delete=models.CASCADE, null=True, blank=True)
#
#     class Meta:
#         managed = False
#         db_table = 'rbac_ud_user_roles'
#         app_label = 'rbac'
#         unique_together = (('rbacuser', 'rbacrole'),)
#         verbose_name = "用户-角色"
#         verbose_name_plural = verbose_name


# class RbacUdRolePermissions(models.Model):
#     # RbacUdRole = models.ForeignKey(RbacUdRole, on_delete=models.CASCADE, null=True, blank=True)
#     # RbacUdPermission = models.ForeignKey(RbacUdPermission, on_delete=models.CASCADE, null=True, blank=True)
#     RbacUdRole = models.ForeignKey(RbacUdRole, on_delete=models.CASCADE, null=True, blank=True)
#     RbacUdPermission = models.ManyToManyField("RbacUdPermission")
#
#     class Meta:
#         managed = False
#         db_table = 'rbac_ud_role_permissions'
#         app_label = 'rbac'
#         # unique_together = (('RbacUdRole', 'RbacUdPermission'),)
#         verbose_name = "角色-权限"
#         verbose_name_plural = verbose_name

# ==============================================================================
# ==============================================================================
# ==============================================================================
