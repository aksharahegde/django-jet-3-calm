from django.contrib import admin
from django.contrib.admin.utils import get_fields_from_path
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory
from django.test import TestCase
from django.utils.encoding import smart_str

from jet.filters import DateRangeFilter
from jet.filters import multiple_choice_list_filter
from jet.filters import RelatedFieldAjaxListFilter
from jet.tests.models import RelatedToTestModel
from jet.tests.models import TestModel


class FiltersTestCase(TestCase):
    def setUp(self):
        self.models = []
        self.factory = RequestFactory()
        self.models.append(TestModel.objects.create(field1="first", field2=1))
        self.models.append(TestModel.objects.create(field1="second", field2=2))

    def get_related_field_ajax_list_filter_params(self):
        model = RelatedToTestModel
        field_path = "field"
        field = get_fields_from_path(model, field_path)[-1]
        lookup_params = {}
        model_admin = admin.site._registry.get(model)

        return field, lookup_params, model, model_admin, field_path

    def test_related_field_ajax_list_filter(self):
        request = self.factory.get("url")
        field, lookup_params, model, model_admin, field_path = (
            self.get_related_field_ajax_list_filter_params()
        )
        list_filter = RelatedFieldAjaxListFilter(
            field, request, lookup_params, model, model_admin, field_path
        )

        self.assertTrue(list_filter.has_output())

        choices = list_filter.field_choices(field, request, model_admin)

        self.assertIsInstance(choices, list)
        self.assertEqual(len(choices), 0)

    def test_related_field_ajax_list_filter_with_initial(self):
        initial = self.models[1]
        request = self.factory.get("url")
        field, lookup_params, model, model_admin, field_path = (
            self.get_related_field_ajax_list_filter_params()
        )
        lookup_params["field__id__exact"] = str(initial.pk)
        list_filter = RelatedFieldAjaxListFilter(
            field, request, lookup_params, model, model_admin, field_path
        )

        self.assertTrue(list_filter.has_output())

        choices = list_filter.field_choices(field, request, model_admin)

        self.assertIsInstance(choices, list)
        self.assertEqual(len(choices), 1)
        self.assertEqual(choices[0], (initial.pk, smart_str(initial)))

    def _get_date_range_filter_params(self, request, lookup_params):
        model = User
        field_path = "date_joined"
        field = get_fields_from_path(model, field_path)[-1]
        model_admin = admin.site._registry.get(model)
        return field, lookup_params, model, model_admin, field_path

    def test_date_range_filter_expected_parameters_and_choices(self):
        request = self.factory.get("url")
        field, lookup_params, model, model_admin, field_path = (
            self._get_date_range_filter_params(request, {})
        )
        list_filter = DateRangeFilter(
            field, request, lookup_params, model, model_admin, field_path
        )

        expected = ["date_joined__gte", "date_joined__lte"]
        self.assertEqual(list_filter.expected_parameters(), expected)

        class ChangeList:
            def get_query_string(self, new_params=None, remove=None):
                return "query-string"

        choices = list(list_filter.choices(ChangeList()))
        self.assertEqual(len(choices), 1)
        self.assertEqual(choices[0]["system_name"], "date-joined")
        self.assertEqual(choices[0]["query_string"], "query-string")

    def test_date_range_filter_make_query_filter_and_get_form_normalization(self):
        request = self.factory.get(
            "url",
            {"date_joined__gte": "2026-01-01", "date_joined__lte": "2026-01-05"},
        )
        field, lookup_params, model, model_admin, field_path = (
            self._get_date_range_filter_params(
                request,
                {
                    "date_joined__gte": ["2026-01-01"],
                    "date_joined__lte": ["2026-01-05"],
                },
            )
        )
        list_filter = DateRangeFilter(
            field, request, lookup_params, model, model_admin, field_path
        )

        self.assertTrue(list_filter.form.is_valid())
        self.assertEqual(
            list_filter.form.cleaned_data["date_joined__gte"].isoformat(), "2026-01-01"
        )
        self.assertEqual(
            list_filter.form.cleaned_data["date_joined__lte"].isoformat(), "2026-01-05"
        )

        query_filter = list_filter._make_query_filter(
            request, list_filter.form.cleaned_data
        )
        self.assertIn("date_joined__gte", query_filter)
        self.assertIn("date_joined__lte", query_filter)
        self.assertEqual(query_filter["date_joined__gte"].hour, 0)
        self.assertEqual(query_filter["date_joined__lte"].hour, 23)

    def test_date_range_filter_queryset_valid_and_invalid(self):
        User.objects.create_user(username="u1", password="x")
        User.objects.create_user(username="u2", password="x")
        valid_request = self.factory.get(
            "url",
            {"date_joined__gte": "2000-01-01", "date_joined__lte": "2100-01-01"},
        )
        field, lookup_params, model, model_admin, field_path = (
            self._get_date_range_filter_params(
                valid_request,
                {"date_joined__gte": "2000-01-01", "date_joined__lte": "2100-01-01"},
            )
        )
        valid_filter = DateRangeFilter(
            field, valid_request, lookup_params, model, model_admin, field_path
        )
        filtered = valid_filter.queryset(valid_request, User.objects.all())
        self.assertEqual(filtered.count(), User.objects.count())

        invalid_request = self.factory.get("url", {"date_joined__gte": "not-a-date"})
        field, lookup_params, model, model_admin, field_path = (
            self._get_date_range_filter_params(
                invalid_request, {"date_joined__gte": "not-a-date"}
            )
        )
        invalid_filter = DateRangeFilter(
            field, invalid_request, lookup_params, model, model_admin, field_path
        )
        unfiltered = invalid_filter.queryset(invalid_request, User.objects.all())
        self.assertEqual(unfiltered.count(), User.objects.count())

    def test_multiple_choice_list_filter_lookup_and_queryset(self):
        filter_class = multiple_choice_list_filter(
            title="field1",
            parameter_name="field1__in",
            lookup_choices=["first", "second"],
        )
        request = self.factory.get("url", {"field1__in": "first,second"})
        params = request.GET.copy()
        list_filter = filter_class(
            request, params, TestModel, admin.site._registry[TestModel]
        )

        lookups = list_filter.lookups(request, admin.site._registry[TestModel])
        self.assertEqual(len(lookups), 2)
        queryset = list_filter.queryset(request, TestModel.objects.all())
        self.assertEqual(queryset.count(), 2)
        self.assertEqual(list_filter.value_as_list(), ["first", "second"])

    def test_multiple_choice_list_filter_choices(self):
        filter_class = multiple_choice_list_filter(
            title="field1",
            parameter_name="field1__in",
            lookup_choices=["first", "second"],
        )
        request = self.factory.get("url", {"field1__in": "first"})
        params = request.GET.copy()
        list_filter = filter_class(
            request, params, TestModel, admin.site._registry[TestModel]
        )

        class ChangeList:
            def get_query_string(self, new_params=None, remove=None):
                if remove:
                    return "removed"
                if not new_params:
                    return "empty"
                return ",".join(sorted([f"{k}={v}" for k, v in new_params.items()]))

        choice_items = list(list_filter.choices(ChangeList()))
        self.assertEqual(choice_items[0]["display"], "Reset")
        first_choice = [
            item for item in choice_items if item.get("display") == "first"
        ][0]
        second_choice = [
            item for item in choice_items if item.get("display") == "second"
        ][0]
        self.assertTrue(first_choice["selected"])
        self.assertIn("field1__in=first,second", second_choice["include_query_string"])
        self.assertEqual(first_choice["exclude_query_string"], "removed")

    def test_multiple_choice_list_filter_requires_choices(self):
        filter_class = multiple_choice_list_filter(title="field1")
        request = self.factory.get("url")
        with self.assertRaises(ImproperlyConfigured):
            filter_class(
                request, request.GET.copy(), TestModel, admin.site._registry[TestModel]
            )
