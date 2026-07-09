import django.utils.timezone
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("jet", "0002_delete_userdashboardmodule"),
    ]

    operations = [
        migrations.CreateModel(
            name="SavedFilterView",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.PositiveIntegerField(verbose_name="user")),
                (
                    "app_label",
                    models.CharField(max_length=100, verbose_name="application"),
                ),
                ("model_name", models.CharField(max_length=100, verbose_name="model")),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                ("query_string", models.TextField(verbose_name="query string")),
                (
                    "date_add",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="date created",
                    ),
                ),
            ],
            options={
                "ordering": ("-date_add",),
                "verbose_name": "saved filter view",
                "verbose_name_plural": "saved filter views",
                "unique_together": {("user", "app_label", "model_name", "name")},
            },
        ),
        migrations.CreateModel(
            name="UserPreferences",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.PositiveIntegerField(unique=True, verbose_name="user")),
                (
                    "theme",
                    models.CharField(blank=True, max_length=50, verbose_name="theme"),
                ),
                (
                    "side_menu_compact",
                    models.BooleanField(
                        blank=True, null=True, verbose_name="compact side menu"
                    ),
                ),
                (
                    "sidebar_pinned",
                    models.BooleanField(
                        blank=True, null=True, verbose_name="pinned sidebar"
                    ),
                ),
                (
                    "date_updated",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
            ],
            options={
                "verbose_name": "user preference",
                "verbose_name_plural": "user preferences",
            },
        ),
    ]
