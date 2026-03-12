import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable

from .models import Proxy


class ProxyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    protocol = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = Proxy
        fields = (
            "pk",
            "id",
            "name",
            "protocol",
            "server",
            "port",
            "description",
        )
        default_columns = (
            "pk",
            "name",
            "protocol",
            "server",
            "port",
            "description",
        )
