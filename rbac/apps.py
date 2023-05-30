from django.apps import AppConfig


class RbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rbac'
    # verbose_name = '菜单和url权限管理'
    verbose_name = '权限系统'
