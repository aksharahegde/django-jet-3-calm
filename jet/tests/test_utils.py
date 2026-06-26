import json
from datetime import date
from datetime import datetime
from unittest import mock

from django.contrib.admin import AdminSite
from django.template import Context
from django.test import TestCase

from jet.tests.models import TestModel
from jet.utils import context_to_dict
from jet.utils import get_admin_site
from jet.utils import get_app_list
from jet.utils import get_menu_item_url
from jet.utils import get_model_instance_label
from jet.utils import get_possible_language_codes
from jet.utils import JsonResponse
from jet.utils import LazyDateTimeEncoder
from jet.utils import user_is_authenticated


class UtilsTestCase(TestCase):
    def test_json_response(self):
        response = JsonResponse({"str": "string", "int": 1})
        response_dict = json.loads(response.content.decode())
        expected_dict = {"int": 1, "str": "string"}
        self.assertEqual(response_dict, expected_dict)
        self.assertEqual(response.get("Content-Type"), "application/json")

    def test_json_response_requires_dict_when_safe(self):
        with self.assertRaises(TypeError):
            JsonResponse(["not", "a", "dict"])

    def test_get_model_instance_label(self):
        field1 = "value"
        field2 = 2
        pinned_application = TestModel.objects.create(field1=field1, field2=field2)
        self.assertEqual(
            get_model_instance_label(pinned_application), "%s%d" % (field1, field2)
        )

    def test_get_app_list(self):
        class User:
            is_active = True
            is_staff = True

            def has_module_perms(self, app):
                return True

            def has_perm(self, object):
                return True

        class Request:
            user = User()

        app_list = get_app_list({"request": Request(), "user": None})

        self.assertIsInstance(app_list, list)

        for app in app_list:
            self.assertIsInstance(app, dict)
            self.assertIsNotNone(app, app.get("models"))
            self.assertIsNotNone(app, app.get("app_url"))
            self.assertIsNotNone(app, app.get("app_label"))

            for model in app["models"]:
                self.assertIsNotNone(app, model.get("object_name"))
                self.assertIsNotNone(app, model.get("name"))

    def test_get_admin_site(self):
        admin_site = get_admin_site({})
        self.assertIsInstance(admin_site, AdminSite)

    def test_lazy_date_time_encoder_dates(self):
        encoder = LazyDateTimeEncoder()

        ts = datetime.now()
        self.assertEqual(encoder.encode(ts), '"%s"' % ts.isoformat())

        ts = date(2015, 5, 3)
        self.assertEqual(encoder.encode(ts), '"%s"' % ts.isoformat())

    def test_lazy_date_time_encoder_dict(self):
        encoder = LazyDateTimeEncoder()
        self.assertEqual(encoder.encode({"key": 1}), '{"key": 1}')

    def test_get_possible_language_codes(self):
        with mock.patch("jet.utils.translation.get_language", return_value="en_us"):
            self.assertEqual(get_possible_language_codes(), ["en-US", "en"])

        with mock.patch("jet.utils.translation.get_language", return_value="fr"):
            self.assertEqual(get_possible_language_codes(), ["fr"])

    def test_user_is_authenticated_property_and_callable(self):
        class PropertyUser:
            is_authenticated = True

        class CallableUser:
            @staticmethod
            def is_authenticated():
                return False

        self.assertTrue(user_is_authenticated(PropertyUser()))
        self.assertFalse(user_is_authenticated(CallableUser()))

    def test_get_menu_item_url_variants(self):
        original_app_list = {
            "tests": {
                "url": "/admin/tests/",
                "models": [{"name": "testmodel", "url": "/admin/tests/testmodel/"}],
            }
        }
        self.assertEqual(
            get_menu_item_url({"type": "app", "app_label": "tests"}, original_app_list),
            "/admin/tests/",
        )
        self.assertEqual(
            get_menu_item_url(
                {"type": "model", "app_label": "tests", "model": "testmodel"},
                original_app_list,
            ),
            "/admin/tests/testmodel/",
        )
        self.assertEqual(
            get_menu_item_url(
                {"type": "reverse", "name": "admin:index"}, original_app_list
            ),
            "/admin/",
        )
        self.assertEqual(
            get_menu_item_url("/custom/url/", original_app_list), "/custom/url/"
        )

    def test_context_to_dict_flattens_context(self):
        flattened = context_to_dict(Context({"a": 1, "b": 2}))
        self.assertEqual(flattened["a"], 1)
        self.assertEqual(flattened["b"], 2)
