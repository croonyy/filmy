from django.db import models
from rbac.util import admin_tools as at
from rbac.util import tools_ud as tu

# Create your models here.
# class Test(models.Model):
#     title = models.CharField(max_length=100, verbose_name='名称', )
#     code = models.JSONField(max_length=1000, verbose_name='源码1', )
#     code2 = models.TextField(max_length=1000, blank=True, null=True,
#                              verbose_name='源码2', )

#     exe_btn = tu.curry(at.set_model_btn, btn_list=[("edit", {}), ])

#     # code2 = ud_admin.UdJsonField(max_length=1000, blank=True, null=True,
#     #                                  verbose_name='源码2', )

#     class Meta:
#         managed = True
#         db_table = 'app1_test'
#         app_label = 'app1'
#         verbose_name = "测试"
#         verbose_name_plural = verbose_name

#     def __unicode__(self):
#         return self.title
