from rest_framework.views import Response, status
from rest_framework.decorators import api_view, schema, permission_classes
from rest_framework import permissions


from rest_framework.decorators import action

from rbac import models as rbac_md
from rbac.drf.serializers import serializer
from rbac.drf.schemas import test_schemas
from rbac.drf.schemas import yasgSchemas
from rbac.drf.serializers.model_serializer import TestSerializer
from rbac.drf.permissions import perm_test
from rbac.drf.responses import response_test

from rest_framework.schemas import AutoSchema
from pprint import pprint

from drf_yasg import openapi
from drf_yasg.openapi import Schema, Response as yasgResponse
from drf_yasg.utils import swagger_auto_schema


# class CustomAutoSchema(AutoSchema):
#     def get_link(self, path, method, base_url):
#         # override view introspection here...
#         pass


@swagger_auto_schema(
    tags=["函数视图测试"],
    method="POST",
    operation_summary="func_view_test",
    operation_description="成功返回 200\n" "失败（参数错误或不符合要求）返回 400",
    # request_body=yasgSchemas.testSchema2,
    request_body=Schema(
            type=openapi.TYPE_OBJECT,
            required=["a"],
            properties={
                "a": Schema(
                    description="a",
                    type=openapi.TYPE_STRING,
                    default="",
                ),
            },
        )
    # manual_parameters=[openapi.Parameter(
    #             "prompt",
    #             openapi.IN_QUERY,
    #             description="输入内容",
    #             required=True,
    #             type=openapi.TYPE_STRING
    #         ),]
    # request_body=TestSerializer, //可以用模型序列化器来充当schema
    # responses=response_test.response_test()
)
@api_view(["POST"])
# @permission_classes((perm_test.loginRequired,))
# @permission_classes([permissions.IsAuthenticated, ])
@permission_classes([])
# @schema(test_schemas.udSchema)  # drf 原生文档用的schema 规则 ，不能设置response的schema
# @action(['GET', 'POST'], detail=False) # 只能在viewset及其子类里面用该装饰器
def func_view_test(request):
    """
    :param request:
    :return: test
    """
    # 原生文档会收集注释显示在接口文档里面
    # print("func_view_test")
    pprint(request)
    # pprint(f"request.body:{request.body}")
    pprint(f"request.GET:{request.GET}")
    pprint(f"request.data:{request.data}")
    pprint(f"request.query_params:{request.query_params}")
    pprint(f"request.user:{request.user}")
    pprint(f"request.user:{request.user.is_authenticated}")
    pprint(f"request.auth:{request.auth}")
    pprint(f"request.method:{request.method}")
    pprint(f"request.content_type:{request.content_type}")

    data = {"aa": "aa"}
    return Response(data=data, status=status.HTTP_200_OK)
    # return Response(data=data)


# @swagger_auto_schema(
#     # tags=['函数视图测试'],
#     method='GET',
#     operation_summary='summary_info',
#     operation_description='成功返回 201\n'
#                           '失败（参数错误或不符合要求）返回 400',
# )
# @action(detail=True, methods=['GET'],
#         # permission_classes=[permissions.IsAuthenticated]
#         )
# @schema(test_schemas.udSchema)
# # @action(['GET', 'POST'], detail=False)
# def func_view_test(request):
#     """
#     :param request:
#     :return: test
#     """
#     print("func_view_test")
#     pprint(request)
#     pprint(f"request.body:{request.body}")
#     pprint(f"request.GET:{request.GET}")
#     pprint(f"request.data:{request.data}")
#     pprint(f"request.query_params:{request.query_params}")
#     pprint(f"request.user:{request.user}")
#     pprint(f"request.auth:{request.auth}")
#     pprint(f"request.method:{request.method}")
#     pprint(f"request.content_type:{request.content_type}")
#
#     data = {"aa": "aa"}
#     return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def UserViewSetPutDelete(request, pk):
    try:
        # filter查询若不存在返回空，get查询不存在抛出异常
        # 这里可以指定查询哪一个字段的数据，可以是name，age等
        user = rbac_md.User.objects.get(User_id=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        u = serializer.UserSerializer(user)
        return Response(data=u.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        u = serializer.UserSerializer(user, data=request.data)
        if u.is_valid():
            u.save()
            return Response(data=u.data, status=status.HTTP_200_OK)
        else:
            return Response(data=u.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# @schema(udSchema)
# # @action(['GET', 'POST'], detail=False)
# def func_view_test(request, pk):
#     try:
#         # filter查询若不存在返回空，get查询不存在抛出异常
#         # 这里可以指定查询哪一个字段的数据，可以是name，age等
#         obj = rbac_md.Test.objects.get(pk=pk)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         test_obj = serializer.TestSerializer(obj)
#         print(f"test_obj:{type(test_obj)}\n{test_obj}")
#         return Response(data=test_obj.data, status=status.HTTP_200_OK)
#     elif request.method == "POST":
#         data = serializer.TestSerializer(data=request.data)
#         if data.is_valid():
#             data.save()
#             return Response(data=data.data, status=status.HTTP_200_OK)
#         else:
#             return Response(data=data.errors, status=status.HTTP_400_BAD_REQUEST)
