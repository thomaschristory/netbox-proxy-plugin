from urllib.parse import urlparse

from django.db.models import Q

# Map client class paths to routing choice values.  NetBox 4.5 passes the
# calling object as ``context['client']``; we inspect its class to decide
# which routing tag applies.
_CLIENT_ROUTING_MAP = {
    # extras.webhooks.send_webhook passes the Webhook model instance
    "extras.models.webhooks.Webhook": "webhooks",
    # core.data_backends – Git, S3, HTTP backends
    "core.data_backends.GitBackend": "data_backends",
    "core.data_backends.S3Backend": "data_backends",
    "core.data_backends.LocalBackend": "data_backends",
    # extras.dashboard.widgets – RSS feed widget
    "extras.dashboard.widgets.RSSFeedWidget": "dashboard_feed",
}


class PluginProxyRouter:
    """
    A proxy router that resolves proxies from the netbox_proxy_plugin database.

    Proxies can be scoped to specific NetBox subsystems via the ``routing``
    field (e.g. "webhooks", "data_backends").  The router inspects the
    ``context['client']`` object (passed by NetBox 4.5's ``resolve_proxies``)
    to determine the subsystem.

    Add to your NetBox configuration (4.5+)::

        PROXY_ROUTERS = [
            "netbox_proxy_plugin.proxy_router.PluginProxyRouter",
            "utilities.proxy.DefaultProxyRouter",
        ]
    """

    @staticmethod
    def _get_protocol_from_url(url):
        return urlparse(url).scheme

    @staticmethod
    def _detect_routing(url, context):
        """Determine the routing tag from the caller context or URL."""
        if context and "client" in context:
            client = context["client"]
            cls = type(client)
            class_path = f"{cls.__module__}.{cls.__qualname__}"
            if class_path in _CLIENT_ROUTING_MAP:
                return _CLIENT_ROUTING_MAP[class_path]
            # Fall back: walk MRO for subclasses of known backends
            for ancestor in cls.__mro__:
                ancestor_path = f"{ancestor.__module__}.{ancestor.__qualname__}"
                if ancestor_path in _CLIENT_ROUTING_MAP:
                    return _CLIENT_ROUTING_MAP[ancestor_path]

        # Heuristic from URL for callers that pass no context (census,
        # release check, plugin catalog).
        if url:
            if "github" in url:
                return "release_check"
            if "plugin" in url or "catalog" in url:
                return "plugin_catalog"

        return None

    def route(self, url=None, protocol=None, context=None):
        from .models import Proxy

        if url and protocol is None:
            protocol = self._get_protocol_from_url(url)

        proxies = Proxy.objects.all()

        if protocol:
            proxies = proxies.filter(protocol=protocol)

        # Narrow by routing tag when we can identify the subsystem.
        routing_type = self._detect_routing(url, context)
        if routing_type:
            proxies = proxies.filter(
                Q(routing__contains=[routing_type]) | Q(routing=[])
            )

        result = {}
        for proxy in proxies:
            result[proxy.protocol] = proxy.url

        return result or None
