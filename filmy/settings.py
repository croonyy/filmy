"""
Django settings for filmy project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z)r7xk_rm1(zw$s8z#ai2m3^s44yr0%t_&cx=*n2l6(nuzby_j'

# SECURITY WARNING: don't run with debug turned on in production!
from filmy import local_config as lc

DEBUG = lc.DEBUG
# DEBUG = False

# DJANGO_DEFAULT = True  #
DJANGO_DEFAULT = False  #

ALLOWED_HOSTS = ["*"]

# yangyuan add on 20230523
CSRF_TRUSTED_ORIGINS = ['http://localhost:8080',
                        # 'http://*',
                        # 'https://*',
                        ]

# LOGIN_REDIRECT_URL = '/rbac/'
# LOGIN_URL = "/admin/login/"
LOGIN_URL = "/"
# LOGOUT_URL = "/admin/logout/"

# LOGIN_REDIRECT_URL = '/'
# LOGIN_URL = "/login/"


# Application definition

INSTALLED_APPS = [
    'simpleui',
    # 'django.contrib.admin',
    'filmy.ud_admin_site.UdAdmin.UdAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ninja',
    'rest_framework',
    'drf_yasg',
]

UD_APPS = [
    'rbac',
    'app1',
]

# api_prefix 接口url前缀
API_PRIFIX='api/v1/'

# 因为我们自定义的认证类，有些接口访问需要使用token，后面就可以在文档中，在请求头中带上token了
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    # 统一设置token
    # 'SECURITY_DEFINITIONS': {
    #     'Token': {
    #         'type': 'apiKey',  #
    #         'name': 'Authorization',
    #         'in': 'header'
    #     },
    # },
    # 'DEFAULT_MODEL_RENDERING': 'example',
    # 'LOGIN_URL': '/api-auth/login/',
    # 'LOGOUT_URL': '/api-auth/logout/',
    'LOGIN_URL': '/admin/login/',
    'LOGOUT_URL': '/admin/logout/',
}

# 认证使用自己定义的认证类（不属于drf-yasg的配置，只是说明上面配置的token是为解决自定义认证存在的403问题
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # 新版drf schema_class默认用的是rest_framework.schemas.openapi.AutoSchema
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

UD_MIDDLEWARE = [
    # 'rbac.util.middleware.PermlistMiddleware',  # 每次请求都查询权限列表太耗资源了，用session只在登录的时候查询一次
    # 'rbac.util.middleware.PermissionMiddleWare',  # 权限校验
    # admin登录登出重定向到自己的登录页面
    # 'rbac.middleware.UdMiddleware.AdminAuthenticationRedirect',
    # 解决跨域
    'rbac.drf.middleware.crossdomainxhr.XsSharing',
    # 解决drf csrf not set, 403 Forbidden:
    'rbac.drf.middleware.csrf_middleware.NotUseCsrfTokenMiddlewareMixin',
    # 'util.middleware.CurrentUserMiddleware',  # 将当前用户存储在线程本地对象中
    # 'rbac.util.middleware.UdMiddleware.WhoDidMiddleware',  # 将当前用户存储在线程本地对象中
    # 'util.middleware.RequestRecordMiddleware',  #
]

ROOT_URLCONF = 'filmy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, "static/reactapp")]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'filmy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        # 'HOST': '192.168.187.189',  # 主机
        'HOST': lc.HOST,  # 主机
        'PORT': '3306',  # 数据库使用的端口
        # 'NAME': 'sino_test',  # 你要存储数据的库名，事先要创建之
        'NAME': 'filmy',  # 你要存储数据的库名，事先要创建之
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456',  # 密码
    },
}
DATABASE_ROUTERS = ['rbac.util.database_router.DatabaseAppsRouter']

DATABASE_APPS_MAPPING = {
    # 'app_name':'database_name'
    # 'admin': 'default',
    # 'rbac': 'default',
    # 'report': 'default',
}

AUTH_USER_MODEL = 'rbac.User'

# ### ldap 配置部分BEGIN ### #
import ldap
from django_auth_ldap.config import LDAPSearch, PosixGroupType

AUTHENTICATION_BACKENDS = (
    # 'django_auth_ldap.backend.LDAPBackend',  # 配置为先使用LDAP认证，如通过认证则不再使用后面的认证方式
    'django.contrib.auth.backends.ModelBackend',  # sso系统中手动创建的用户也可使用，优先级靠后。注意这2行的顺序
)

AUTH_LDAP_SERVER_URI = 'ldap://192.168.100.99:389'
AUTH_LDAP_BASE_DN = 'ou=三诺生物传感股份有限公司,dc=sinocare,dc=com'
# AUTH_LDAP_BASE_DN = 'dc=sinocare,dc=com'
AUTH_LDAP_BIND_DN = 'cn=ser_ldapbudisrv,ou=特殊帐号,dc=sinocare,dc=com'
AUTH_LDAP_BIND_PASSWORD = 'TbyN4h&^elUXhCHY'
# 用户的DN是uid=caojun,ou=People,dc=ldap,dc=ssotest,dc=net，所以用uid
AUTH_LDAP_USER_SEARCH = LDAPSearch(AUTH_LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")
# AUTH_LDAP_USER_SEARCH = LDAPSearch(AUTH_LDAP_BASE_DN, ldap.SCOPE_SUBTREE)
# print(ldap.SCOPE_SUBTREE)
AUTH_LDAP_ALWAYS_UPDATE_USER = True  # This is the default, but I like to be explicit.
AUTH_LDAP_CACHE_TIMEOUT = 100  # ldap缓存时间AUTH_LDAP_CACHE_TIMEOUT = 100 #ldap缓存时间

AUTH_LDAP_USER_ATTR_MAP = {  # key为数据库字段名，value为ldap中字段名，此字典解决django model与ldap字段名可能出现的不一致问题
    "username": "sAMAccountName",
    # "name": "givenName",
    "email": "userPrincipalName",
    "first_name": "name",
    "last_name": "sn",
    "chinese_name": "name",
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-Hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

# USE_TZ = True
USE_TZ = False

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DOMAIN = '172.9.100.161:9977'

# CSRF_TRUSTED_ORIGINS = ['https://django.sinocare.com']

# 跨域开启者策略
# SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'  # 默认值
# SECURE_CROSS_ORIGIN_OPENER_POLICY = None  # None  或者'None' 都行
SECURE_CROSS_ORIGIN_OPENER_POLICY = '*'  # None  或者'None' 都行

STATIC_URL = '/static/'  # 代表html模板{% static "pet/fonts/flaticon/flaticon.css" %} 里面的static的url根路由
MEDIA_URL = '/media/'  # 代表html模板{% media "pet/fonts/flaticon/flaticon.css" %} 里面的media的url根路由
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace("\\", "/")

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, "reactapp/"),
    # os.path.join(BASE_DIR, "reactapp/myapp/build/static"),
    # os.path.join(BASE_DIR, "reactapp/report"),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS.append(os.path.join(BASE_DIR, 'static'))

if DEBUG:
    STATIC_ROOT = ''
else:
    STATICFILES_DIRS.pop(STATICFILES_DIRS.index(os.path.join(BASE_DIR, 'static')))

if not DJANGO_DEFAULT:
    INSTALLED_APPS = INSTALLED_APPS + UD_APPS
    MIDDLEWARE = MIDDLEWARE + UD_MIDDLEWARE
    # AUTH_USER_MODEL = 'rbac.User'
    # for app_name in UD_APPS:
    #     if app_name not in DATABASE_APPS_MAPPING.keys():
    #         DATABASE_APPS_MAPPING[app_name] = 'default'
else:
    pass

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 此选项开启表示禁用部分日志，不建议设置为True
    'formatters': {
        'standard_format': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d]' + \
                      '[task_id:%(name)s][%(filename)s:%(lineno)d] ' + \
                      '[%(levelname)s]- %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(message)s'  # 日志格式
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'ud_format': {
            'format': '[%(pathname)s:%(lineno)d]\n[%(levelname)s][%(asctime)s] %(message)s'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',  # 过滤器，只有当setting的DEBUG = True时生效
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'ud_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'ud_format'
        },
        # 'file': {  # 重点配置部分
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     # 'filename': '/home/lockey23/myapp/myapp/debug.log',  # 日志保存文件
        #     'filename': 'test.log',  # 日志保存文件
        #     'formatter': 'verbose'  # 日志格式，与上边的设置对应选择
        # }
    },
    'loggers': {
        'django': {  # 日志记录器
            # 'handlers': ['file'],
            'handlers': ['console'],
            # 'level': 'DEBUG',
            'level': 'INFO',
            'propagate': True,
        },
        'ud_logger': {  # 日志记录器
            'handlers': ['ud_console'],
            'level': 'INFO',
            'propagate': True,
        }
    },
}

# NINJA_DOCS_VIEW = 'redoc'


# simpleui
SIMPLEUI_HOME_INFO = False  # 去掉右边的信息
# SIMPLEUI_DEFAULT_THEME = "e-red.css"
SIMPLEUI_LOGO = "/static/img/logo/logo.png"
SIMPLEUI_ICON = {
    # '用户': 'fab fa-apple',
    # '员工管理': 'fas fa-user-tie'
    # "Report": "fas fa-chart-line",
    # fas fa-clipboard

    # "Report": "fas fa-clipboard",
    # "SS看板推送": "fas fa-chart-line",
    #
    # "Slice元素": "fas fa-cog",  # fas fa-cogs fas fa-cog
    # "查询": "fas fa-cog",
    # "看板": "fas fa-cog",
    #
    # "Sino": "fas fa-tags",
    # "公众号推送": "fa fa-th-list",
    # "指标分解": "fas fa-tag",
    # "机器人推送": "fa fa-th-list",
    # "权限检查": 'fas fa-check-circle',
    "Crud": "fas fa-cubes",
    "数据库连接信息": "fab fa-connectdevelop",
    "Clickhouse表对象": "fas fa-tags"

}
