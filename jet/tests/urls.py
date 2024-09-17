from django.contrib import admin
from django.urls import include
from django.urls import re_path

admin.autodiscover()

urlpatterns = [
    re_path(r"^jet/", include("jet.urls", "jet")),
    re_path(r"^jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
    re_path(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    re_path("admin/", admin.site.urls),
]
