import django_filters
from netbox.filtersets import NetBoxModelFilterSet

from .models import Proxy, ProxyProtocolChoices


class ProxyFilterSet(NetBoxModelFilterSet):
    protocol = django_filters.MultipleChoiceFilter(
        choices=ProxyProtocolChoices,
    )

    class Meta:
        model = Proxy
        fields = ("id", "name", "protocol", "server", "port")

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
