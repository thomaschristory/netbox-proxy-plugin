from netbox.plugins import PluginConfig


class NetboxProxiesConfig(PluginConfig):
    name = "netbox_proxies"
    verbose_name = "Proxies"
    description = "Manage HTTP proxy configurations for NetBox"
    version = "0.1.0"
    author = "thomaschristory"
    base_url = "proxies"
    min_version = "4.2.0"


config = NetboxProxiesConfig
