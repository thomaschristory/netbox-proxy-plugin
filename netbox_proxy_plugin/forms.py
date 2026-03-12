from django import forms as django_forms
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField

from .models import Proxy, ProxyProtocolChoices, ProxyRoutingChoices


class ProxyForm(NetBoxModelForm):
    comments = CommentField()
    routing = django_forms.MultipleChoiceField(
        choices=ProxyRoutingChoices,
        required=False,
        help_text="NetBox subsystems that should use this proxy. Leave empty for all.",
    )

    class Meta:
        model = Proxy
        fields = (
            "name",
            "protocol",
            "server",
            "port",
            "username",
            "password",
            "routing",
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
            "routing",
            "description",
        )


class ProxyFilterForm(NetBoxModelFilterSetForm):
    model = Proxy
    protocol = ProxyProtocolChoices
    routing = django_forms.MultipleChoiceField(
        choices=ProxyRoutingChoices,
        required=False,
    )
