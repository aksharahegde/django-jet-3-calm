import datetime
from collections import OrderedDict
from zoneinfo import ZoneInfo

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import RelatedFieldListFilter
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.utils import get_model_from_relation
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ImproperlyConfigured
from django.forms.utils import flatatt
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import smart_str
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext as _


class RelatedFieldAjaxListFilter(RelatedFieldListFilter):
    template = "jet/related_field_ajax_list_filter.html"
    ajax_attrs = None

    def has_output(self):
        return True

    def field_choices(self, field, request, model_admin):
        model = (
            field.remote_field.model
            if hasattr(field, "remote_field")
            else field.related_field.model
        )
        app_label = model._meta.app_label
        model_name = model._meta.object_name

        self.ajax_attrs = format_html(
            "{0}",
            flatatt(
                {
                    "data-app-label": app_label,
                    "data-model": model_name,
                    "data-ajax--url": reverse("jet:model_lookup"),
                    "data-queryset--lookup": self.lookup_kwarg,
                }
            ),
        )

        if self.lookup_val is None:
            return []

        other_model = get_model_from_relation(field)
        if hasattr(field, "rel"):
            rel_name = field.rel.get_related_field().name
        else:
            rel_name = other_model._meta.pk.name

        # Handle case where lookup_val might be a list (e.g., ['28'] instead of '28')
        lookup_value = self.lookup_val
        if isinstance(lookup_value, list) and len(lookup_value) > 0:
            lookup_value = lookup_value[0]

        queryset = model._default_manager.filter(**{rel_name: lookup_value}).all()
        return [(x._get_pk_val(), smart_str(x)) for x in queryset]


class DateRangeFilter(admin.filters.FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_gte = f"{field_path}__gte"
        self.lookup_kwarg_lte = f"{field_path}__lte"

        super().__init__(field, request, params, model, model_admin, field_path)

        self.form = self.get_form(request)

    def get_timezone(self):
        return timezone.get_default_timezone()

    @staticmethod
    def make_dt_aware(value):
        if settings.USE_TZ:
            # The following settings are not part of the standard Django settings,
            # but they have been left in for backward compatibility.
            # If `ACT_ZONEINFO` is not set, it will fallback to `settings.TIME_ZONE`.
            if hasattr(settings, "ACT_ZONEINFO"):
                act_zoneinfo = settings.ACT_ZONEINFO
            else:
                try:
                    act_zoneinfo = ZoneInfo(settings.TIME_ZONE)
                except (AttributeError, TypeError):
                    act_zoneinfo = timezone.get_default_timezone()

            # If `UTC_ZONEINFO` is not set, it will fallback to UTC.
            if hasattr(settings, "UTC_ZONEINFO"):
                utc_zoneinfo = settings.UTC_ZONEINFO
            else:
                utc_zoneinfo = ZoneInfo("UTC")

            value = value.replace(tzinfo=act_zoneinfo).astimezone(utc_zoneinfo)

        return value

    def choices(self, cl):
        yield {
            "system_name": slugify(self.title),
            "query_string": cl.get_query_string({}, remove=self._get_expected_fields()),
        }

    def expected_parameters(self):
        return self._get_expected_fields()

    def queryset(self, request, queryset):
        if self.form.is_valid():
            validated_data = dict(self.form.cleaned_data.items())
            if validated_data:
                return queryset.filter(
                    **self._make_query_filter(request, validated_data)
                )
        return queryset

    def _get_expected_fields(self):
        return [self.lookup_kwarg_gte, self.lookup_kwarg_lte]

    def _make_query_filter(self, request, validated_data):
        query_params = {}
        date_value_gte = validated_data.get(self.lookup_kwarg_gte, None)
        date_value_lte = validated_data.get(self.lookup_kwarg_lte, None)

        if date_value_gte:
            query_params[f"{self.field_path}__gte"] = self.make_dt_aware(
                datetime.datetime.combine(date_value_gte, datetime.time.min),
            )
        if date_value_lte:
            query_params[f"{self.field_path}__lte"] = self.make_dt_aware(
                datetime.datetime.combine(date_value_lte, datetime.time.max),
            )

        return query_params

    def get_template(self):
        return "rangefilter/date_filter.html"

    template = property(get_template)

    def get_form(self, request):
        form_class = self._get_form_class()

        # Normalize self.used_parameters to ensure all values are single values
        normalized_parameters = {
            key: value[0] if isinstance(value, list) else value
            for key, value in self.used_parameters.items()
        }

        return form_class(normalized_parameters)

    def _get_form_class(self):
        fields = self._get_form_fields()

        form_class = type("DateRangeForm", (forms.BaseForm,), {"base_fields": fields})
        form_class.media = self._get_media()

        return form_class

    def _get_form_fields(self):
        return OrderedDict(
            (
                (
                    self.lookup_kwarg_gte,
                    forms.DateField(
                        label="",
                        widget=AdminDateWidget(attrs={"placeholder": _("From date")}),
                        localize=True,
                        required=False,
                    ),
                ),
                (
                    self.lookup_kwarg_lte,
                    forms.DateField(
                        label="",
                        widget=AdminDateWidget(attrs={"placeholder": _("To date")}),
                        localize=True,
                        required=False,
                    ),
                ),
            )
        )

    @staticmethod
    def _get_media():
        js = [
            "calendar.js",
            "admin/DateTimeShortcuts.js",
        ]
        css = [
            "widgets.css",
        ]
        return forms.Media(
            js=["admin/js/%s" % url for url in js],
            css={"all": ["admin/css/%s" % path for path in css]},
        )


def multiple_choice_list_filter(**kwargs):
    class MultipleChoiceListFilter(SimpleListFilter):
        """
        Configuration:
            A dict. containing following data:
                - title (required): Label for filter
                - parameter_name (optional; title will be considered):
                    db column name
                - lookup_choices (list of strings)

        e.g.: multiple_choice_list_filter(**{
            'title': 'status',
            'parameter_name': 'status__in',
            'lookup_choices': [o1, o2, o3]
        })

        version: 1.0.0
        - List Choice filter with multiple value selection support
        - lookups method should be defined in child class
        version: 2.0.0
        - Checkbox UI for selecting values to prevent page refresh on every
            selection
        - Option to pass kwargs for config. instead of creating subclass
        """

        title = _(kwargs.pop("title", None))
        parameter_name = kwargs.pop("parameter_name", None)
        if parameter_name is None:
            parameter_name = "%s__in" % title
        lookup_choices = kwargs.pop("lookup_choices", None)
        template = "jet/multiple_choice_list_filter.html"

        def lookups(self, request, model_admin):
            """
            returns: a list of tuples (value, verbose value)
            """
            if not self.lookup_choices:
                raise ImproperlyConfigured(_("Choices are mandatory"))

            lookup_options = [(c, c) for c in self.lookup_choices]
            return sorted(lookup_options, key=lambda x: x[1])

        def queryset(self, request, queryset):
            if request.GET.get(self.parameter_name):
                extra_kwargs = {
                    self.parameter_name: request.GET[self.parameter_name].split(",")
                }
                queryset = queryset.filter(**extra_kwargs)
            return queryset

        def value_as_list(self):
            return self.value().split(",") if self.value() else []

        def choices(self, changelist):
            def amend_query_string(include=None, exclude=None):
                selections = self.value_as_list()
                if include and include not in selections:
                    selections.append(include)
                if exclude and exclude in selections:
                    selections.remove(exclude)
                if selections:
                    csv = ",".join(selections)
                    return changelist.get_query_string({self.parameter_name: csv})
                else:
                    return changelist.get_query_string(remove=[self.parameter_name])

            yield {
                "selected": self.value() is None,
                "query_string": changelist.get_query_string(
                    remove=[self.parameter_name]
                ),
                "display": "Reset",
                "reset": True,
            }
            for lookup, title in self.lookup_choices:
                yield {
                    "selected": str(lookup) in self.value_as_list(),
                    "query_string": changelist.get_query_string(
                        {self.parameter_name: lookup}
                    ),
                    "include_query_string": amend_query_string(include=str(lookup)),
                    "exclude_query_string": amend_query_string(exclude=str(lookup)),
                    "display": title,
                }

    return MultipleChoiceListFilter
