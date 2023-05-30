from django.utils.html import format_html
from django.utils.safestring import mark_safe
from rbac.util.tools_ud import set_func_attr
from django.db.models import JSONField
from django.forms import widgets
import json
import logging
from django import forms
from django.forms.utils import flatatt

from django.contrib import admin

logger = logging.getLogger(__name__)


class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'insight_db'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


def ModelAdminGenerator():
    cls = type('ModelAdmin', (admin.ModelAdmin,), {})
    return cls


def generate_media_class(js_path_tuple):
    cls = type('Media', (), {})
    cls.js = js_path_tuple
    return cls


def generate_media_class_by_dict(static_dict):
    cls = type('Media', (), {})
    if 'js' in static_dict.keys():
        cls.js = static_dict['js']
    if 'css' in static_dict.keys():
        cls.css = static_dict['css']
    return cls


btn_dict = {
    "edit": lambda x: """
            <button type="button" class="el-button el-button--primary button-ud" 
                onclick="window.open('/admin/{app_name}/{model_name}/{id}/change/','_self')" ">
                <span>编辑</span>
            </button>
            """.format(app_name=x._meta.app_label, model_name=x.__class__.__name__.lower(), id=x.id),
    # format增加层数就要嵌套{{}}
    "dispatch": lambda x: """
            <button type="button" class="{{class}}" 
                onclick="dispatch('{{url}}','{id}','{cls_name}','{{tag}}');" url="">
            <!-- <i class="el-icon-plus"></i> -->
                <span>{{btn_name}}</span>
            </button>
            """.format(id=x.id, cls_name=x.__class__.__name__),
}


@set_func_attr({"short_description": format_html('<a href="#">操作</a>')})
def set_model_btn(self, btn_list=[("edit", {}), ]):
    btn_str_list = []
    for temp, dic in btn_list:
        default = lambda x: ''
        tmp_str = (btn_dict.get(temp) or default)(self)
        btn_str_list.append(tmp_str.format(**dic))
    btn_str = """<div>{}</div>""".format('\n'.join(btn_str_list))
    # return format_html(btn_str)
    return mark_safe(btn_str)


@set_func_attr({"short_description": format_html('<a href="#">操作</a>')})
def exe_btn(self):
    temp = """
    <button type="button" class="el-button el-button--primary button-ud" 
        onclick="window.open('/admin/{app_name}/{model_name}/{id}/change/','_self')" ">
        <span>编辑</span>
    </button>
    <button type="button" class="el-button el-button--primary button-ud" 
        onclick="exe_by_tag('{id}','{model_name}','{tag}');" url="">
        <span>执行</span>
    </button>
    """
    return format_html(temp.format(app_name=self._meta.app_label,
                                   model_name=self.__class__.__name__.lower(),
                                   id=self.pk,
                                   tag="ClickhouseTable#auto_def_crud_perms"))


class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        # print(f"prettyformat_value:{type(value)}:{value}")
        try:
            value = json.dumps(json.loads(value), indent=2,
                               ensure_ascii=False, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            # logger.warning("Error while formatting JSON: {}".format(e))
            return super().format_value(value)


# class JsonAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         JSONField: {'widget': PrettyJSONWidget}
#     }


def menu_view(view):

    # def ud_changelist_view(self, request, extra_content=None):
    def ud_changelist_view(self, request, *args, **kwargs):
        return view(request, *args, **kwargs)

    return ud_changelist_view
