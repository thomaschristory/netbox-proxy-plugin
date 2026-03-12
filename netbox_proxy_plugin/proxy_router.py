from urllib.parse import urlparse

from django.db.models import Q


class PluginProxyRouter:
    """
    A proxy router that resolves proxies from the netbox_proxy_plugin database.

    Proxies can be scoped to specific NetBox subsystems via the ``routing``
    field (e.g. "webhooks", "data_backends"). When ``context`` contains a
    ``type`` key, only proxies whose routing list includes that type (or
    proxies with an empty routing list, meaning "all") are returned.

    Add to your NetBox configuration::

        PROXY_ROUTERS = [
            "netbox_proxy_plugin.proxy_router.PluginProxyRouter",
            "utilities.proxy.DefaultProxyRouter",
        ]
    """

    @staticmethod
    def _get_protocol_from_url(url):
        return urlparse(url).scheme

    def route(self, url=None, protocol=None, context=None):
        from .models import Proxy

        if url and protocol is None:
            protocol = self._get_protocol_from_url(url)

        proxies = Proxy.objects.all()

        if protocol:
            proxies = proxies.filter(protocol=protocol)

        # Filter by routing context when provided.
        if context and "type" in context:
            routing_type = context["type"]
            proxies = proxies.filter(Q(routing__contains=[routing_type]) | Q(routing=[]))

        result = {}
        for proxy in proxies:
            result[proxy.protocol] = proxy.url

        return result or None
