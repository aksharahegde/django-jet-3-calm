from django.contrib.admin import RelatedFieldListFilter, SimpleListFilter
from django.utils.encoding import smart_str
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.admin.utils import get_model_from_relation
from django.forms.utils import flatatt


class RelatedFieldAjaxListFilter(RelatedFieldListFilter):
    template = 'jet/related_field_ajax_list_filter.html'
    ajax_attrs = None

    def has_output(self):
        return True

    def field_choices(self, field, request, model_admin):
        model = field.remote_field.model if hasattr(field, 'remote_field') else field.related_field.model
        app_label = model._meta.app_label
        model_name = model._meta.object_name

        self.ajax_attrs = format_html('{0}', flatatt({
            'data-app-label': app_label,
            'data-model': model_name,
            'data-ajax--url': reverse('jet:model_lookup'),
            'data-queryset--lookup': self.lookup_kwarg
        }))

        if self.lookup_val is None:
            return []

        other_model = get_model_from_relation(field)
        if hasattr(field, 'rel'):
            rel_name = field.rel.get_related_field().name
        else:
            rel_name = other_model._meta.pk.name

        queryset = model._default_manager.filter(**{rel_name: self.lookup_val}).all()
        return [(x._get_pk_val(), smart_str(x)) for x in queryset]


try:
    from collections import OrderedDict
    from django import forms
    from django.contrib.admin.widgets import AdminDateWidget
    from django.utils.translation import gettext_lazy as _
    from rangefilter.filter import DateRangeFilter as OriginalDateRangeFilter


    class DateRangeFilter(OriginalDateRangeFilter):
        def get_template(self):
            return 'rangefilter/date_filter.html'

        def _get_form_fields(self):
            # this is here, because in parent DateRangeFilter AdminDateWidget
            # could be imported from django-suit
            return OrderedDict((
                (self.lookup_kwarg_gte, forms.DateField(
                    label='',
                    widget=AdminDateWidget(attrs={'placeholder': _('From date')}),
                    localize=True,
                    required=False
                )),
                (self.lookup_kwarg_lte, forms.DateField(
                    label='',
                    widget=AdminDateWidget(attrs={'placeholder': _('To date')}),
                    localize=True,
                    required=False
                )),
            ))

        @staticmethod
        def _get_media():
            css = [
                'style.css',
            ]
            return forms.Media(
                css={'all': ['range_filter/css/%s' % path for path in css]}
            )
except ImportError:
    pass




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
        title = _(kwargs.pop('title', None))
        parameter_name = kwargs.pop('parameter_name', None)
        if parameter_name is None:
            parameter_name = '%s__in' % title
        lookup_choices = kwargs.pop('lookup_choices', None)
        template = 'jet/multiple_choice_list_filter.html'

        def lookups(self, request, model_admin):
            """
            returns: a list of tuples (value, verbose value)
            """
            if not self.lookup_choices:
                ImproperlyConfigured(_('Choices are mandatory'))

            lookup_options = [(c, c) for c in self.lookup_choices]
            return sorted(lookup_options, key=lambda x: x[1])

        def queryset(self, request, queryset):
            if request.GET.get(self.parameter_name):
                extra_kwargs = {
                    self.parameter_name: request.GET[self.parameter_name].split(',')
                }
                queryset = queryset.filter(**extra_kwargs)
            return queryset

        def value_as_list(self):
            return self.value().split(',') if self.value() else []

        def choices(self, changelist):

            def amend_query_string(include=None, exclude=None):
                selections = self.value_as_list()
                if include and include not in selections:
                    selections.append(include)
                if exclude and exclude in selections:
                    selections.remove(exclude)
                if selections:
                    csv = ','.join(selections)
                    return changelist.get_query_string({self.parameter_name: csv})
                else:
                    return changelist.get_query_string(remove=[self.parameter_name])

            yield {
                'selected': self.value() is None,
                'query_string': changelist.get_query_string(
                    remove=[self.parameter_name]),
                'display': 'Reset',
                'reset': True,
            }
            for lookup, title in self.lookup_choices:
                yield {
                    'selected': str(lookup) in self.value_as_list(),
                    'query_string': changelist.get_query_string(
                        {self.parameter_name: lookup}),
                    'include_query_string': amend_query_string(include=str(lookup)),
                    'exclude_query_string': amend_query_string(exclude=str(lookup)),
                    'display': title,
                }
    return MultipleChoiceListFilter