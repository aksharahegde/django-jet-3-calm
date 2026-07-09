from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Bookmark(models.Model):
    url = models.URLField(verbose_name=_("URL"))
    title = models.CharField(verbose_name=_("title"), max_length=255)
    user = models.PositiveIntegerField(verbose_name=_("user"))
    date_add = models.DateTimeField(
        verbose_name=_("date created"), default=timezone.now
    )

    class Meta:
        verbose_name = _("bookmark")
        verbose_name_plural = _("bookmarks")
        ordering = ("date_add",)

    def __str__(self):
        return self.title


class PinnedApplication(models.Model):
    app_label = models.CharField(verbose_name=_("application name"), max_length=255)
    user = models.PositiveIntegerField(verbose_name=_("user"))
    date_add = models.DateTimeField(
        verbose_name=_("date created"), default=timezone.now
    )

    class Meta:
        verbose_name = _("pinned application")
        verbose_name_plural = _("pinned applications")
        ordering = ("date_add",)

    def __str__(self):
        return self.app_label


class SavedFilterView(models.Model):
    user = models.PositiveIntegerField(verbose_name=_("user"))
    app_label = models.CharField(max_length=100, verbose_name=_("application"))
    model_name = models.CharField(max_length=100, verbose_name=_("model"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    query_string = models.TextField(verbose_name=_("query string"))
    date_add = models.DateTimeField(
        verbose_name=_("date created"), default=timezone.now
    )

    class Meta:
        verbose_name = _("saved filter view")
        verbose_name_plural = _("saved filter views")
        ordering = ("-date_add",)
        unique_together = ("user", "app_label", "model_name", "name")

    def __str__(self):
        return self.name


class UserPreferences(models.Model):
    user = models.PositiveIntegerField(verbose_name=_("user"), unique=True)
    theme = models.CharField(max_length=50, verbose_name=_("theme"), blank=True)
    side_menu_compact = models.BooleanField(
        verbose_name=_("compact side menu"), null=True, blank=True
    )
    sidebar_pinned = models.BooleanField(
        verbose_name=_("pinned sidebar"), null=True, blank=True
    )
    date_updated = models.DateTimeField(
        verbose_name=_("date updated"), auto_now=True
    )

    class Meta:
        verbose_name = _("user preference")
        verbose_name_plural = _("user preferences")

    def __str__(self):
        return str(self.user)
