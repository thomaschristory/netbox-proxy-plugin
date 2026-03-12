from netbox.api.routers import NetBoxRouter

from .views import ProxyViewSet

router = NetBoxRouter()
router.register("proxies", ProxyViewSet)
urlpatterns = router.urls
