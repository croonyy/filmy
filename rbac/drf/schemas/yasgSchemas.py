from drf_yasg import openapi
from drf_yasg.openapi import Schema, Response

# def gen_schema(type,required):
def gen_schema():
    return Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh_token"],
            properties={
                "refresh_token": Schema(
                    description="refresh_token",
                    type=openapi.TYPE_STRING,
                    default="",
                ),
            },
        )


testSchema = Schema(
    type=openapi.TYPE_OBJECT,
    required=['account_id'],
    properties={
        'uid': Schema(
            description='用户id example: 12345',
            type=openapi.TYPE_INTEGER,
            default=12345,
        ),
        'telephone': Schema(
            description='手机号码 example: 13711225566',
            type=openapi.TYPE_STRING,
            default='13711225566',
        ),
        'code': Schema(
            description='兑换码 example: 15462fd',
            type=openapi.TYPE_STRING,
            default='15462fd',
        ),
    },
)

testSchema2 = Schema(
    type=openapi.TYPE_OBJECT,
    required=['account_id'],
    properties={
        'id': Schema(
            description='id example: 12354',
            type=openapi.TYPE_INTEGER),
        # 'testSchema': testSchema,
    },
)

loginSchema = Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', "password"],
    properties={
        'username': Schema(
            description='用户名 example: yuan.yang',
            type=openapi.TYPE_STRING,
            default="yuan.yang",
        ),
        'password': Schema(
            description='密码 example: abc_123,.',
            type=openapi.TYPE_STRING,
            default='123456',
        ),
    },
)


refreshSchema = Schema(
    type=openapi.TYPE_OBJECT,
    required=['refresh_token'],
    properties={
        'refresh_token': Schema(
            description='refresh_token',
            type=openapi.TYPE_STRING,
            default="",
        ),
    },
)



# 	@swagger_auto_schema(
#         operation_summary='xxx',
#         operation_description="",
#         manual_parameters=[
#             openapi.Parameter(
#                 "prompt",
#                 openapi.IN_QUERY,
#                 description="输入内容",
#                 required=True,
#                 type=openapi.TYPE_STRING
#             ),
#             openapi.Parameter(
#                 "model",
#                 openapi.IN_QUERY,
#                 description="识别",
#                 type=openapi.TYPE_STRING,
#                 default="test"
#             ),
#             openapi.Parameter(
#                 "max_tokens",
#                 openapi.IN_QUERY,
#                 description="限制长度",
#                 type=openapi.TYPE_INTEGER,
#                 default=2000
#             ),
#         ],
#         responses={200: "ok", "data": "xxx返回内容"}
#     )
# ————————————————
# 版权声明：本文为CSDN博主「三人行ylc」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/test_cyl/article/details/128361301


#  @swagger_auto_schema(
#         operation_summary='新增用户收货地址', 
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 "provice_id": openapi.Schema(
#                     description='省id',
#                     type=openapi.TYPE_STRING,
#                     required="true"
#                 ),
#                 "city_id": openapi.Schema(
#                     description='市id',
#                     type=openapi.TYPE_STRING,
#                     required="true"
#                 ),
#                 'district_id': openapi.Schema(
#                     type=openapi.TYPE_STRING,
#                     description='区id',
#                     required="true"
#                 ),
#                 'title': openapi.Schema(
#                     type=openapi.TYPE_STRING,
#                     description='地址标题',
#                     required="true"
#                 ),
#                 'receiver': openapi.Schema(
#                     type=openapi.TYPE_STRING,
#                     description='收货地址',
#                     required="true"
#                 ),
#                 'place': openapi.Schema(
#                     type=openapi.TYPE_STRING,
#                     description='详细地址',
#                     required="true"
#                 ),
#                 'mobile': openapi.Schema(
#                     type=openapi.TYPE_STRING,
#                     description='手机号',
#                     required="true"
#                 ),
#                 'tel': openapi.Schema(
#                     type=openapi.TYPE_STRING,
#                     description='固定电话',
#                     required="false"
#                 ),
#                 'email': openapi.Schema(
#                     type=openapi.TYPE_STRING,
#                     description='电子邮箱',
#                     required="false"
#                 )
#             }
#         ),
#         responses={200: "ok", "data": ""}
#     )
# ————————————————
# 版权声明：本文为CSDN博主「三人行ylc」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/test_cyl/article/details/128361301
