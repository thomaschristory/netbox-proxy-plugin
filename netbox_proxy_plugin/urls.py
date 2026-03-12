from django.urls import include, path
from utilities.urls import get_model_urls

from . import views  # noqa: F401 - views must be imported to register model views

urlpatterns = [
    path("proxies/", include(get_model_urls("netbox_proxy_plugin", "proxy", detail=False))),
    path("proxies/<int:pk>/", include(get_model_urls("netbox_proxy_plugin", "proxy"))),
]
