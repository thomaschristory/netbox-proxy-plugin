import django.contrib.postgres.fields
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("extras", "0123_journalentry_kind_default"),
    ]

    operations = [
        migrations.CreateModel(
            name="Proxy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("protocol", models.CharField(max_length=10)),
                ("server", models.CharField(max_length=255)),
                ("port", models.PositiveIntegerField()),
                ("username", models.CharField(blank=True, max_length=255)),
                ("password", models.CharField(blank=True, max_length=255)),
                (
                    "routing",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=50),
                        blank=True,
                        default=list,
                        help_text="NetBox subsystems that should use this proxy. Leave empty for all.",
                        size=None,
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=200)),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "verbose_name_plural": "proxies",
                "ordering": ("name",),
            },
        ),
    ]
