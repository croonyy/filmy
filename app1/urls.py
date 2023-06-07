# from django.conf.urls import url
from app1.drf import views
from app1.drf.views import authentication


from django.urls import path, re_path, include
from filmy.views import icon_admin


# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

from filmy.settings import API_PRIFIX

p = lambda x: API_PRIFIX + x


prefix = API_PRIFIX

urlpatterns = [
    #test
    path("test/", icon_admin, name="test"),
    path(p("test/"), icon_admin, name="test"),
    
    # drf接口
    path(p("login/"), authentication.login),
    path(p("logout/"), authentication.logout),
    path(p("refresh_token/"), authentication.refresh_token),
]
