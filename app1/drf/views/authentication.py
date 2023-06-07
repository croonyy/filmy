from rest_framework.views import Response, status
from rest_framework.decorators import api_view, schema, permission_classes
from rest_framework import permissions

from rbac.drf.schemas import yasgSchemas
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from rbac.util import jwt_auth as ja
import traceback
from django.contrib.auth import login as admin_login, logout as admin_logout
from django.views.decorators.csrf import csrf_exempt
from rbac.util.tools_ud import timer


# @csrf_exempt
@swagger_auto_schema(
    tags=['函数视图测试'],
    method='POST',
    operation_summary='login',
    operation_description='成功返回 200\n'
                          '失败（参数错误或不符合要求）返回 400',
    request_body=yasgSchemas.loginSchema,
    # request_body=TestSerializer, //可以用模型序列化器来充当schema
    # responses=response_test.response_test()
)
@api_view(['POST'])
# @permission_classes((perm_test.loginRequired,))
# @permission_classes([permissions.IsAuthenticated, ])
def login(request):
    """
    Login and retun a token:\n
    To login please provide:
     - **username**
     - **password**
     - text **username:str** *password:Str*
    """
    print("*" * 40 + "api login" + "*" * 40)
    username = request.data['username']
    password = request.data['password']
    if not (username and password):
        data = {"status": 0, "error": "username or password is empty",
                "msg": "username or password is empty"}
        return Response(data=data, status=status.HTTP_200_OK)
    try:
        user = authenticate(request, username=username, password=password)
        print(f"crud login.")
        print(f"user:{user}")
        if not user:
            raise Exception("login failed,username or password is wrong.")
        if not user.is_staff:
            user.is_staff = True
            user.save()
        print(f"user.is_staff:{user.is_staff}")
        token_info = ja.create_token({"username": user.username})
        token_info['status'] = 1
        admin_login(request, user, backend=None)
        print(f"admin login.")
        print("*" * 40 + "api login finished" + "*" * 40)
        return Response(data=token_info, status=status.HTTP_200_OK)
    except Exception as e:
        msg = f"error:\n{str(e)}\ntraceback:\n{traceback.format_exc()}"
        print(msg)
        print("*" * 40 + "api login finished" + "*" * 40)
        data = {"status": 0, "error": str(e), "msg": msg}
        return Response(data=data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    tags=['函数视图测试'],
    method='GET',
    operation_summary='logout',
    operation_description='成功返回 200\n'
                          '失败（参数错误或不符合要求）返回 400',
)
@api_view(['GET'])
def logout(request):  # login_form: LoginForm=Form(...) 让请求参数以表单形式显示，不用就是json文本格式
    """
    Logiout
    """
    admin_logout(request)  # 调用admin的logout
    data = {"status": 1, "msg": "后台退出登录成功"}
    return Response(data=data, status=status.HTTP_200_OK)



@swagger_auto_schema(
    tags=['函数视图测试'],
    method='POST',
    operation_summary=' ',
    operation_description='成功返回 200\n'
                          '失败（参数错误或不符合要求）返回 400',
    request_body=yasgSchemas.refreshSchema,
    # request_body=TestSerializer, //可以用模型序列化器来充当schema
    # responses=response_test.response_test()
)
@api_view(['POST'])
# @csrf_exempt
# @requires_csrf_token
# @permission_classes((perm_test.loginRequired,))
# @permission_classes([permissions.IsAuthenticated, ])
def refresh_token(request):
    try:
        # print(f"refresh_token:{refresh_token}")
        refresh_token = request.data['refresh_token']
        info = ja.parse_payload(refresh_token)
        # print(info)
        if info['status']:
            token_info = ja.create_token({"username": info['data']['username']})
            token_info['status'] = 1
            return Response(data=token_info, status=status.HTTP_200_OK)
        else:
            data = {"status": 0, "msg": "parse_payload failed."}
            return Response(data=data, status=status.HTTP_200_OK)
    except Exception as e:
        msg = f"error:\n{str(e)}\ntraceback:\n{traceback.format_exc()}"
        # print(msg)
        data = {"status": 0, "msg": msg}
        # print(data)
        return Response(data=data, status=status.HTTP_200_OK)