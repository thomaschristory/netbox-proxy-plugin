from netbox.api.viewsets import NetBoxModelViewSet

from ..filtersets import ProxyFilterSet
from ..models import Proxy
from .serializers import ProxySerializer


class ProxyViewSet(NetBoxModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer
    filterset_class = ProxyFilterSet
