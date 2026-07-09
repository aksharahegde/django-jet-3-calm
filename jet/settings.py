from django.conf import settings


def get_setting(name, default=None):
    return getattr(settings, name, default)


# Theme (defaults for backwards compatibility; prefer get_setting() at runtime)
JET_DEFAULT_THEME = get_setting("JET_DEFAULT_THEME", "default")
JET_THEMES = get_setting("JET_THEMES", [])

# Side menu
JET_SIDE_MENU_COMPACT = get_setting("JET_SIDE_MENU_COMPACT", False)
JET_SIDE_MENU_ITEMS = get_setting("JET_SIDE_MENU_ITEMS", None)
JET_SIDE_MENU_CUSTOM_APPS = get_setting("JET_SIDE_MENU_CUSTOM_APPS", None)

# Improved usability
JET_CHANGE_FORM_SIBLING_LINKS = get_setting("JET_CHANGE_FORM_SIBLING_LINKS", True)
