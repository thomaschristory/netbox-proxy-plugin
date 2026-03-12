import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable

from .models import Proxy, ProxyRoutingChoices


class RoutingColumn(tables.Column):
    """Display routing choices as a comma-separated list of labels."""

    def render(self, value):
        if not value:
            return "All"
        labels = {c[0]: c[1] for c in ProxyRoutingChoices.CHOICES}
        return ", ".join(labels.get(v, v) for v in value)


class ProxyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    protocol = ChoiceFieldColumn()
    routing = RoutingColumn()

    class Meta(NetBoxTable.Meta):
        model = Proxy
        fields = (
            "pk",
            "id",
            "name",
            "protocol",
            "server",
            "port",
            "routing",
            "description",
        )
        default_columns = (
            "pk",
            "name",
            "protocol",
            "server",
            "port",
            "routing",
            "description",
        )
