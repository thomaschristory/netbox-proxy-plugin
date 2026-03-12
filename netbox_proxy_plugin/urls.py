from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from utilities.urls import get_model_urls

from . import models

urlpatterns = [
    *get_model_urls("netbox_proxy_plugin", models.Proxy),
]
