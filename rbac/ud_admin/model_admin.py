from django.contrib.admin.options import ModelAdmin, FORMFIELD_FOR_DBFIELD_DEFAULTS
import copy
from rbac.ud_admin import fields, widgets
from django.db import models

# 原始对象
# FORMFIELD_FOR_DBFIELD_DEFAULTS = {
#     models.DateTimeField: {
#         "form_class": forms.SplitDateTimeField,
#         "widget": widgets.AdminSplitDateTime,
#     },
#     models.DateField: {"widget": widgets.AdminDateWidget},
#     models.TimeField: {"widget": widgets.AdminTimeWidget},
#     models.TextField: {"widget": widgets.AdminTextareaWidget},
#     models.URLField: {"widget": widgets.AdminURLFieldWidget},
#     models.IntegerField: {"widget": widgets.AdminIntegerFieldWidget},
#     models.BigIntegerField: {"widget": widgets.AdminBigIntegerFieldWidget},
#     models.CharField: {"widget": widgets.AdminTextInputWidget},
#     models.ImageField: {"widget": widgets.AdminFileWidget},
#     models.FileField: {"widget": widgets.AdminFileWidget},
#     models.EmailField: {"widget": widgets.AdminEmailInputWidget},
#     models.UUIDField: {"widget": widgets.AdminUUIDInputWidget},
# }

UD_FORMFIELD = {
    models.JSONField: {'widget': widgets.AceWidget(mode="json", theme="iplastic")},
    fields.UdSqlField: {"widget": widgets.AceWidget(mode="sql", theme="dracula")}
}


class UdModelAdmin(ModelAdmin):

    def __init__(self, *args, **kwargs):
        # for k, v in UD_FORMFIELD.items():
        #     self.formfield_overrides.update(k, v)
        super().__init__(*args, **kwargs)
        for k, v in UD_FORMFIELD.items():
            self.formfield_overrides.setdefault(k, {}).update(v)
