from netbox.api.serializers import NetBoxModelSerializer

from ..models import Proxy


class ProxySerializer(NetBoxModelSerializer):
    class Meta:
        model = Proxy
        fields = (
            "id",
            "url",
            "display",
            "name",
            "protocol",
            "server",
            "port",
            "username",
            "routing",
            "description",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "name", "protocol")
