from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("api/", include("apps.hotel.urls")),
    path("api/", include("apps.embassy.urls")),
    path("api/auth/", include("apps.auth.urls")),
]
