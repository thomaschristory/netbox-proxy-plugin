from netbox.choices import ButtonColorChoices
from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

proxy_items = (
    PluginMenuItem(
        link="plugins:netbox_proxy_plugin:proxy_list",
        link_text="Proxies",
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_proxy_plugin:proxy_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:netbox_proxy_plugin:proxy_bulk_import",
                title="Import",
                icon_class="mdi mdi-upload",
                color=ButtonColorChoices.CYAN,
            ),
        ),
    ),
)

menu = PluginMenu(
    label="Proxies",
    groups=(("Proxy Management", proxy_items),),
    icon_class="mdi mdi-server-network",
)
