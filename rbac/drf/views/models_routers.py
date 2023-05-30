from rbac.drf.views import model_view_test as mvs

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('test', mvs.TestViewSet)
# router.register('permission', mvs.PermissionViewSet)
