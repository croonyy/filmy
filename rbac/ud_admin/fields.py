from django.db import models

from rbac.ud_admin import widgets as ud_widgets

# class UdTextField(models.TextField):
#     def test(self):
#         print('test')

from django.db import models
import ast
import json
from django.core import exceptions
from django.utils.translation import gettext_lazy as _


# class UdTextField(models.TextField):
class UdTextField(models.Field):
    """自定义list字段
    models.SubfieldBase   提供to_python   和 from_db_value
    把数据库数据转化成python数据
    现在主要是from_db_value 方法 把数据库数据转化成python数据
    to_python 主要是接受form表单
    """
    # __metacalss__ = models.SubfieldBase
    description = 'Stores a python list'

    def __init__(self, *args, **kwargs):
        super(UdTextField, self).__init__(*args, **kwargs)

        # def db_type(self, connection):
        #     if connection.setting_dict['ENGINE'] == 'django.db.backends.mysql':
        #         return 'listtype'

    def from_db_value(self, value, expression, connection, context):

        """数据库数据转成python数据"""
        if value is None:
            value = []
            return value
            if isinstance(value, list):
                return value
            return ast.literal_eval(value)

    def to_python(self, value):
        """从数据库中读取的数据转成python
        eval（value）读取value原来的类型
        ast模块就是帮助Python应用来处理抽象的语法解析的。
        而该模块下的literal_eval()函数：
        则会判断需要计算的内容计算后是不是合法的python类型，
        如果是则进行运算，否则就不进行运算。
        """
        if not value:
            value = []
        if isinstance(value, list):
            return value
        return ast.literal_eval(value)

    def get_prep_value(self, value):
        """
        把python数据压缩后保存到数据库
        或者说把python对象转化成查询值
        返回值是个字符串
        :param value:
        :return:
        """
        if value is None:
            return value
        return str(value)

    # def get_db_prep_value(self, value, connection, prepared=False):
    #     """把查询集数据转化成数据库值   一般不需要重写 只需要覆盖"""
    #     value = super(ListField, self).get_db_prep_value()
    #     if value is not None:
    #         return connection.Database.Binary(value)
    #     return value
    #

    def get_prep_lookup(self, lookup_type, value):
        """限制查询方式"""
        if lookup_type == 'exact':
            return value
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            return TypeError('lookup type %r not supported' % lookup_type)

            def value_to_string(self, obj):

                """转换字段数据以进行序列化
            Field._get_val_from_obj(obj) 是获取值序列化的最佳方式
            """
                value = self._get_val_from_obj(obj)
                return self.get_db_prep_value(value)


class UdSqlField(models.TextField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_python(self, value):  # 将数据库内容转为python对象时调用
        print(f"to_python:{type(value)}:{value}")
        # value = value.split('\n')
        # value = str(value)
        # print(f"to_python:{value}")
        # return value.replace('\n', '\n')
        return super().to_python(value)

    # def from_db_value(self, value, expression, connection):  # 从数据库读取字段值时调用
    #     print(f"from_db_value:{type(value)}:{value}")
    #     # value = self.format_value(value)
    #     # return value
    #     return super().from_db_value(value, expression, connection)

    def get_prep_value(self, value):  # 保存时插入数据, 转为字符串存储
        print(f"get_prep_value:{type(value)}:{value}")
        return super().get_prep_value(value)
        # return value


def check_json_format(raw_msg):
    """
    用于判断一个字符串是否符合Json格式

    :param self:

    :return:

    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            # json.loads(raw_msg, encoding='utf-8')
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False


class UdModJsonField(models.JSONField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UdJsonField(models.JSONField):
    # empty_strings_allowed = False
    # description = _("A JSON object")
    # default_error_messages = {
    #     "invalid": _("Value must be valid JSON."),
    # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format_value(self, value):
        # print(f"format_value:{type(value)}:{value}")
        try:
            value = json.loads(value, encoding='utf8')
            # value = value.replace('\n', '\n')
            value = json.dumps(value, indent=2,
                               ensure_ascii=False, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            # row_lengths = [len(r) for r in value.split('\n')]
            # self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            # self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            # logger.warning("Error while formatting JSON: {}".format(e))
            return value

    def validate(self, value, model_instance):  # 保存时提交表单数据验证
        # print(f"validate:{type(value)}:{value}")
        if not check_json_format(value):
            raise exceptions.ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )
        super().validate(value, model_instance)

    def to_python(self, value):  # 将数据库内容转为python对象时调用
        # print(f"to_python:{type(value)}:{value}")
        # value = value.split('\n')
        # value = str(value)
        # print(f"to_python:{value}")
        # return value.replace('\n', '\n')
        return super().to_python(value)

    def from_db_value(self, value, expression, connection):  # 从数据库读取字段值时调用
        # print(f"from_db_value:{type(value)}:{value}")
        # value = self.format_value(value)
        # return value
        return super().from_db_value(value, expression, connection)

    def get_prep_value(self, value):  # 保存时插入数据, 转为字符串存储
        # print(f"get_prep_value:{type(value)}:{value}")
        return super().get_prep_value(value)
        # return value

    def value_to_string(self, obj):  # Rest Framework调用时
        # print(f"value_to_string:obj:{type(obj)}:{obj}")
        return super().value_to_string(obj)

    # def value_to_string(self, obj):  # Rest Framework调用时
    #     return self.value_from_object(obj)
