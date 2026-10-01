from django.contrib import admin
from django.urls import include, path

from apps.embassy.views.citizen_register import citizen_register, citizen_register_success

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("api/", include("apps.hotel.urls")),
    path("api/", include("apps.embassy.urls")),
    path("api/auth/", include("apps.auth.urls")),
    path("citizen/register/", citizen_register, name="citizen_register"),
    path("citizen/register/success/", citizen_register_success, name="citizen_register_success"),
]
