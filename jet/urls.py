from django.urls import re_path
from django.views.i18n import JavaScriptCatalog

javascript_catalog = JavaScriptCatalog.as_view()

from jet.views import (
    add_bookmark_view,
    delete_saved_filter_view,
    get_preferences_view,
    list_saved_filter_views,
    model_lookup_view,
    navigation_lookup_view,
    remove_bookmark_view,
    save_filter_view,
    save_preferences_view,
    toggle_application_pin_view,
)


app_name = "jet"

urlpatterns = [
    re_path(r"^add_bookmark/$", add_bookmark_view, name="add_bookmark"),
    re_path(r"^remove_bookmark/$", remove_bookmark_view, name="remove_bookmark"),
    re_path(
        r"^toggle_application_pin/$",
        toggle_application_pin_view,
        name="toggle_application_pin",
    ),
    re_path(r"^model_lookup/$", model_lookup_view, name="model_lookup"),
    re_path(r"^navigation_lookup/$", navigation_lookup_view, name="navigation_lookup"),
    re_path(
        r"^saved_filter_views/$", list_saved_filter_views, name="list_saved_filter_views"
    ),
    re_path(r"^save_filter_view/$", save_filter_view, name="save_filter_view"),
    re_path(
        r"^delete_saved_filter_view/$",
        delete_saved_filter_view,
        name="delete_saved_filter_view",
    ),
    re_path(r"^preferences/$", get_preferences_view, name="get_preferences"),
    re_path(r"^save_preferences/$", save_preferences_view, name="save_preferences"),
    re_path(
        r"^jsi18n/$",
        javascript_catalog,
        {"packages": "django.contrib.admin+jet"},
        name="jsi18n",
    ),
]
