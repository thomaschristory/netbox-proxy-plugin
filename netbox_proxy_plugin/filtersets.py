import django_filters
from netbox.filtersets import NetBoxModelFilterSet

from .models import Proxy, ProxyProtocolChoices, ProxyRoutingChoices


class ProxyFilterSet(NetBoxModelFilterSet):
    protocol = django_filters.MultipleChoiceFilter(
        choices=ProxyProtocolChoices,
    )
    routing = django_filters.MultipleChoiceFilter(
        choices=ProxyRoutingChoices,
        lookup_expr="contains",
    )

    class Meta:
        model = Proxy
        fields = ("id", "name", "protocol", "server", "port", "routing")

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
