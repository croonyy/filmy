from rest_framework.views import Response, status, APIView
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from rbac import models as rbac_md
from rest_framework.schemas import AutoSchema
from rbac.drf.schemas.test_schemas import udSchema
from rbac.drf.serializers import serializer
from rest_framework.decorators import action
from rest_framework import viewsets, mixins
import json
from pprint import pprint
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_yasg.openapi import Schema, Response


# class test_view(APIView):
#     def get(self, request, pk):
#         try:
#             obj = rbac_md.Test.objects.get(pk=pk)
#         except:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         json_data = serializer.TestSerializer(instance=obj)
#         return Response(data=json_data.data, status=status.HTTP_200_OK)


class class_view_test(APIView):
    schema = udSchema

    @swagger_auto_schema(
        tags=['自定义类视图测试'],
        operation_description='没模型get',
        operation_summary=' ', )
    def get(self, request):
        # req_param = json.loads(request.body)
        print(dir(request))
        pprint(f"request.body:{request.body}")
        pprint(f"request.GET:{request.GET}")
        pprint(f"request.data:{request.data}")
        pprint(f"request.query_params:{request.query_params}")
        return Response(data={"aa": "aa"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['自定义类视图测试'],
        operation_description='没模型post',
        operation_summary=' ',
        request_body=Schema(type=openapi.TYPE_OBJECT,
                            required=['account_id'],
                            properties={
                                'account_id': Schema(
                                    description='用户id example: 12354',
                                    type=openapi.TYPE_INTEGER),
                                'telephone': Schema(
                                    description='手机号码 example: 19811111111',
                                    type=openapi.TYPE_STRING),
                                'code': Schema(
                                    description='兑换码 example: 15462fd',
                                    type=openapi.TYPE_STRING),
                                'disguise_change': Schema(
                                    description='是否是伪变化 example: 0表示不是,1 表示是',
                                    type=openapi.TYPE_INTEGER, enum=[0, 1]),
                            }),
        responses={
            400: Response(description='操作失败', examples={'json': {'code': -1, 'msg': '失败原因'}}),
            200: Response(description='操作成功', examples={'json': {'code': 0, 'msg': '成功'}})
        }
    )
    def post(self, request):
        # req_param = json.loads(request.body)
        pprint(request)
        pprint(f"request.body:{request.body}")
        pprint(f"request.GET:{request.GET}")
        pprint(f"request.data:{request.data}")
        pprint(f"request.query_params:{request.query_params}")
        pprint(f"request.user:{request.user}")
        pprint(f"request.auth:{request.auth}")
        pprint(f"request.method:{request.method}")
        pprint(f"request.content_type:{request.content_type}")
        # for k in dir(request):
        #     print(k)
        #     print(k, getattr(request, k.lower()))
        pprint({k: str(getattr(request, k)) for k in dir(request)})
        # pprint(dir(request))
        return Response(data={"aa": "aa"}, status=status.HTTP_200_OK)

    def handle_exception(self, exc):
        print(f"exception:{type(exc)}\n{exc}")

        return Response(data={"status": "failed"}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, schema=udSchema)
    def clean(self, *args, **kwargs):
        return Response({"aa": "aa"})
