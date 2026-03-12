from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField

from .models import Proxy, ProxyProtocolChoices


class ProxyForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = Proxy
        fields = (
            "name",
            "protocol",
            "server",
            "port",
            "username",
            "password",
            "description",
            "tags",
            "comments",
        )


class ProxyImportForm(NetBoxModelImportForm):
    class Meta:
        model = Proxy
        fields = (
            "name",
            "protocol",
            "server",
            "port",
            "username",
            "password",
            "description",
        )


class ProxyFilterForm(NetBoxModelFilterSetForm):
    model = Proxy
    protocol = ProxyProtocolChoices
