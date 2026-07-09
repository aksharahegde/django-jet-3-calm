from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

from jet.forms import AddBookmarkForm
from jet.forms import ModelLookupForm
from jet.forms import RemoveBookmarkForm
from jet.forms import SaveFilterViewForm
from jet.forms import ToggleApplicationPinForm
from jet.forms import UserPreferencesForm
from jet.models import Bookmark
from jet.models import SavedFilterView
from jet.models import UserPreferences
from jet.utils import JsonResponse
from jet.utils import get_menu_items
from jet.utils import user_is_authenticated


def _staff_user(request):
    return user_is_authenticated(request.user) and request.user.is_staff


def _build_navigation_items(request):
    items = []
    context = {"request": request, "user": request.user}

    for app in get_menu_items(context):
        if not app.get("has_perms", True):
            continue

        app_label = app.get("label", app.get("name", ""))
        for model in app.get("items", []):
            if model.get("has_perms", True) and model.get("url"):
                model_label = model.get("name", model.get("label", ""))
                items.append(
                    {
                        "type": "model",
                        "label": "%s › %s" % (app_label, model_label),
                        "url": model["url"],
                    }
                )

        if app.get("url"):
            items.append(
                {
                    "type": "app",
                    "label": app_label,
                    "url": app["url"],
                }
            )

    for bookmark in Bookmark.objects.filter(user=request.user.pk):
        items.append(
            {
                "type": "bookmark",
                "label": bookmark.title,
                "url": bookmark.url,
            }
        )

    return items


@require_POST
def add_bookmark_view(request):
    result = {"error": False}
    form = AddBookmarkForm(request, request.POST)

    if form.is_valid():
        bookmark = form.save()
        result.update({"id": bookmark.pk, "title": bookmark.title, "url": bookmark.url})
    else:
        result["error"] = True

    return JsonResponse(result)


@require_POST
def remove_bookmark_view(request):
    result = {"error": False}

    try:
        instance = Bookmark.objects.get(pk=request.POST.get("id"))
        form = RemoveBookmarkForm(request, request.POST, instance=instance)

        if form.is_valid():
            form.save()
        else:
            result["error"] = True
    except Bookmark.DoesNotExist:
        result["error"] = True

    return JsonResponse(result)


@require_POST
def toggle_application_pin_view(request):
    result = {"error": False}
    form = ToggleApplicationPinForm(request, request.POST)

    if form.is_valid():
        pinned = form.save()
        result["pinned"] = pinned
    else:
        result["error"] = True

    return JsonResponse(result)


@require_GET
def model_lookup_view(request):
    result = {"error": False}

    form = ModelLookupForm(request, request.GET)

    if form.is_valid():
        items, total = form.lookup()
        result["items"] = items
        result["total"] = total
    else:
        result["error"] = True

    return JsonResponse(result)


@require_GET
def navigation_lookup_view(request):
    if not _staff_user(request):
        return JsonResponse({"error": True, "items": []})

    query = request.GET.get("q", "").strip().lower()
    items = _build_navigation_items(request)

    if query:
        items = [item for item in items if query in item["label"].lower()]

    return JsonResponse({"error": False, "items": items[:50]})


@require_GET
def list_saved_filter_views(request):
    if not _staff_user(request):
        return JsonResponse({"error": True, "items": []})

    app_label = request.GET.get("app_label", "")
    model_name = request.GET.get("model_name", "")
    filters = SavedFilterView.objects.filter(
        user=request.user.pk, app_label=app_label, model_name=model_name
    )
    items = [
        {
            "id": item.pk,
            "name": item.name,
            "query_string": item.query_string,
        }
        for item in filters
    ]
    return JsonResponse({"error": False, "items": items})


@require_POST
def save_filter_view(request):
    if not _staff_user(request):
        return JsonResponse({"error": True})

    form = SaveFilterViewForm(request, request.POST)
    if form.is_valid():
        saved = form.save()
        return JsonResponse(
            {
                "error": False,
                "id": saved.pk,
                "name": saved.name,
                "query_string": saved.query_string,
            }
        )
    return JsonResponse({"error": True})


@require_POST
def delete_saved_filter_view(request):
    if not _staff_user(request):
        return JsonResponse({"error": True})

    try:
        item = SavedFilterView.objects.get(
            pk=request.POST.get("id"), user=request.user.pk
        )
        item.delete()
        return JsonResponse({"error": False})
    except SavedFilterView.DoesNotExist:
        return JsonResponse({"error": True})


@require_GET
def get_preferences_view(request):
    if not _staff_user(request):
        return JsonResponse({"error": True})

    try:
        prefs = UserPreferences.objects.get(user=request.user.pk)
        return JsonResponse(
            {
                "error": False,
                "theme": prefs.theme,
                "side_menu_compact": prefs.side_menu_compact,
                "sidebar_pinned": prefs.sidebar_pinned,
            }
        )
    except UserPreferences.DoesNotExist:
        return JsonResponse(
            {
                "error": False,
                "theme": "",
                "side_menu_compact": None,
                "sidebar_pinned": None,
            }
        )


@require_POST
def save_preferences_view(request):
    if not _staff_user(request):
        return JsonResponse({"error": True})

    form = UserPreferencesForm(request, request.POST)
    if form.is_valid():
        prefs = form.save()
        return JsonResponse(
            {
                "error": False,
                "theme": prefs.theme,
                "side_menu_compact": prefs.side_menu_compact,
                "sidebar_pinned": prefs.sidebar_pinned,
            }
        )
    return JsonResponse({"error": True})
