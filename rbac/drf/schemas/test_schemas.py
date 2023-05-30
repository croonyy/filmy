from rest_framework.schemas import ManualSchema
from rest_framework.compat import coreapi, coreschema
from django.utils.html import format_html

udSchema = ManualSchema(
    description=format_html('<h4 style="color:red">接口文档测试</h1>'),
    fields=[
        coreapi.Field(name="id",
                      # required=True,
                      location="query",
                      schema=coreschema.Integer(description="主键id")
                      ),
        coreapi.Field(name="param1",
                      required=False,
                      location="query",
                      schema=coreschema.Enum(enum=[1, 2],
                                             description="类型(1:删除, 2:填充均值)")
                      ),
        coreapi.Field(name="param2",
                      required=False,
                      location="query",
                      schema=coreschema.String(max_length=10, min_length=None, )
                      ),
        coreapi.Field(name="param3",
                      required=False,
                      location="query",
                      schema=coreschema.Object()
                      ),
        # coreapi.Field(name="param3",
        #               required=False,
        #               location="query",
        #               schema=coreschema.Object()
        #               )
    ]
)
#
# udSchema2 = ManualSchema(
#     description=format_html('<h4 style="color:red">接口文档测试</h1>'),
#     fields=[
#         coreapi.Field(name="id",
#                       # required=True,
#                       location="query",
#                       schema=coreschema.Integer(description="主键id")
#                       ),
#         coreapi.Field(name="param1",
#                       required=False,
#                       location="query",
#                       schema=coreschema.
#                       )
#
#     ]
# )
