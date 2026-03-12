from urllib.parse import urlparse


class PluginProxyRouter:
    """
    A proxy router that resolves proxies from the netbox_proxies plugin database.

    Add to your NetBox configuration:
        PROXY_ROUTERS = [
            "netbox_proxies.proxy_router.PluginProxyRouter",
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

        result = {}
        for proxy in proxies:
            result[proxy.protocol] = proxy.url

        return result or None
