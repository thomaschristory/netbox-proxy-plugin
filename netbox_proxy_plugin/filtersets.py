import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet

from .models import Proxy, ProxyProtocolChoices, ProxyRoutingChoices


class ProxyFilterSet(NetBoxModelFilterSet):
    protocol = django_filters.MultipleChoiceFilter(
        choices=ProxyProtocolChoices,
    )
    routing = django_filters.MultipleChoiceFilter(
        choices=ProxyRoutingChoices,
        method="filter_routing",
    )

    class Meta:
        model = Proxy
        fields = ("id", "name", "protocol", "server", "port", "routing")

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    def filter_routing(self, queryset, name, value):
        if not value:
            return queryset
        q = Q()
        for v in value:
            q |= Q(routing__contains=[v])
        return queryset.filter(q)
