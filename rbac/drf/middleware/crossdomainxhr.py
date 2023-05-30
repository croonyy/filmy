from django import http

from django.utils.deprecation import MiddlewareMixin

# 由于复杂请求时，首先会发送“预检”请求，如果“预检”成功，则发送真实数据。
#
# “预检”请求时，允许请求方式则需服务器设置响应头：Access-Control-Request-Method
# “预检”请求时，允许请求头则需服务器设置响应头：Access-Control-Request-Headers
# “预检”缓存时间，服务器设置响应头：Access-Control-Max-Age

# crossdomain
XS_SHARING_ALLOWED_ORIGINS = '*'
# XS_SHARING_ALLOWED_ORIGINS = 'http://127.0.0.1:8081'
XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'PUT', 'DELETE', 'OPTIONS']
XS_SHARING_ALLOWED_HEADERS = ['Content-Type', '*']
XS_SHARING_ALLOWED_CREDENTIALS = 'true'


class XsSharing(MiddlewareMixin):
    """
    This middleware allows cross-domain XHR using the html5 postMessage API.

    Access-Control-Allow-Origin: http://foo.example
    Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE

    Based off https://gist.github.com/426829
    """

    def process_request(self, request):
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
            response['Access-Control-Allow-Headers'] = ",".join(XS_SHARING_ALLOWED_HEADERS)
            response['Access-Control-Allow-Credentials'] = XS_SHARING_ALLOWED_CREDENTIALS
            return response
        return None

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
        response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
        response['Access-Control-Allow-Headers'] = ",".join(XS_SHARING_ALLOWED_HEADERS)
        response['Access-Control-Allow-Credentials'] = XS_SHARING_ALLOWED_CREDENTIALS
        response["Access-Control-Max-Age"] = "1000"  # 用来指定本次预检请求的有效期，单位为秒，，在此期间不用发出另一条预检请求。
        return response
