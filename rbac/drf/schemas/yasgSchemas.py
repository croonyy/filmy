from drf_yasg import openapi
from drf_yasg.openapi import Schema, Response

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
        'testSchema': testSchema,
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
