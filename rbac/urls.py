# from django.conf.urls import url

from rbac import views as rbac_views

from rbac.drf import views
from rbac.drf.views import authentication

from rbac.drf.views.models_routers import router

from django.urls import path, re_path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="croonyy API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="yuan.yang@sinocare.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(r'', rbac_views.index, name='index'),

    path('test1/', rbac_views.test, name='test1'),

    # def文档
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),

    # drf接口
    path('model_view_test/', include(router.urls)),
    re_path(r'^class_view_test/$', views.class_view_test.class_view_test.as_view()),
    re_path(r'^func_view_test/$', views.func_view_test.func_view_test),
    # re_path(r'^login/$', views.authentication.login),
    # re_path(r'^logout/$', views.authentication.logout),
    re_path(r'^login/$', authentication.login),
    re_path(r'^logout/$', authentication.logout),

]
