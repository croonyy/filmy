from rest_framework import viewsets, mixins
from rbac import models as md
from rbac.drf.serializers import model_serializer as ms

from rest_framework.decorators import action
from rest_framework.views import Response

from rbac.drf.schemas.test_schemas import udSchema

from drf_yasg.utils import swagger_auto_schema


# class TestViewSet(viewsets.ReadOnlyModelViewSet):
# class TestViewSet(mixins.CreateModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin,
#                   mixins.ListModelMixin,
#                   viewsets.GenericViewSet):
# class TestViewSet(viewsets.ModelViewSet):
#     """
#     list：
#         查询所有模型
#
#     create：
#         新增模型
#
#     retrieve：
#         查询单个模型
#
#     update：
#         更新模型
#
#     destroy：
#         删除模型
#     """
#     queryset = md.Test.objects.all()
#     serializer_class = ms.TestSerializer
#
#     @action(methods=['get'], detail=False, schema=udSchema)
#     def ud_action_test(self, *args, **kwargs):
#         return Response({"aa": "aa"})


class TestViewSet(viewsets.ModelViewSet):
    queryset = md.Test.objects.all()
    serializer_class = ms.TestSerializer
    # pagination_class = LargeResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'delete']
    # http_method_names = ['get', 'post', 'put', 'delete', 'patch']
    tag = ['模型[Test]类视图测试']

    @swagger_auto_schema(tags=tag,
                         operation_summary='查询所有模型operation_summary',
                         operation_description='查询所有模型operation_description')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=tag,
                         operation_summary='查询单个模型operation_summary',
                         operation_description='查询单个模型operation_description')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=tag,
                         operation_summary='新增模型operation_summary',
                         operation_description='新增模型operation_description')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=tag,
                         operation_summary='更新模型operation_summary',
                         operation_description='更新模型operation_description')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=tag,
                         operation_summary='删除模型operation_summary',
                         operation_description='删除模型operation_description')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PermissionViewSet(viewsets.ModelViewSet):
    """
    list：查询所有模型
    create：新增模型
    retrieve：查询单个模型
    update：更新模型
    destroy：删除模型
    """
    tag = ['模型[Permission]类视图测试']
    queryset = md.Permission.objects.all()
    serializer_class = ms.PermissionSerializer
    # pagination_class = LargeResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'delete']

    @swagger_auto_schema(tags=tag,
                         operation_summary='查询所有模型operation_summary',
                         operation_description='查询所有模型operation_description')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=tag,
                         operation_summary='查询单个模型operation_summary',
                         operation_description='查询单个模型operation_description')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=tag,
                         operation_summary='新增模型operation_summary',
                         operation_description='新增模型operation_description')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=tag,
                         operation_summary='更新模型operation_summary',
                         operation_description='更新模型operation_description')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=tag,
                         operation_summary='删除模型operation_summary',
                         operation_description='删除模型operation_description')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
