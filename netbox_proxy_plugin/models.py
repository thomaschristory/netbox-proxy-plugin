from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet


class ProxyProtocolChoices(ChoiceSet):
    key = "Proxy.protocol"

    CHOICES = [
        ("http", "HTTP", "blue"),
        ("https", "HTTPS", "green"),
        ("socks4", "SOCKS4", "orange"),
        ("socks5", "SOCKS5", "purple"),
    ]


class ProxyRoutingChoices(ChoiceSet):
    key = "Proxy.routing"

    CHOICES = [
        ("webhooks", "Webhooks", "blue"),
        ("data_backends", "Data Backends", "green"),
    ]


class Proxy(NetBoxModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    protocol = models.CharField(
        max_length=10,
        choices=ProxyProtocolChoices,
    )
    server = models.CharField(
        max_length=255,
        help_text="Proxy server address (e.g. proxy.example.com)",
    )
    port = models.PositiveIntegerField()
    username = models.CharField(
        max_length=255,
        blank=True,
    )
    password = models.CharField(
        max_length=255,
        blank=True,
    )
    routing = ArrayField(
        base_field=models.CharField(max_length=50),
        blank=True,
        default=list,
        help_text="NetBox subsystems that should use this proxy. Leave empty for all.",
    )
    description = models.CharField(
        max_length=200,
        blank=True,
    )

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "proxies"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_proxy_plugin:proxy", args=[self.pk])

    @property
    def url(self):
        """Build the full proxy URL."""
        if self.username:
            return f"{self.protocol}://{self.username}:{self.password}@{self.server}:{self.port}"
        return f"{self.protocol}://{self.server}:{self.port}"
