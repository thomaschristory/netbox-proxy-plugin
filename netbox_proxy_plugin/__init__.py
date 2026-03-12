from netbox.plugins import PluginConfig


class NetboxProxyPluginConfig(PluginConfig):
    name = "netbox_proxy_plugin"
    verbose_name = "Proxies"
    description = "Manage HTTP proxy configurations for NetBox"
    version = "0.1.0"
    author = "thomaschristory"
    base_url = "proxies"
    min_version = "4.2.0"


config = NetboxProxyPluginConfig
