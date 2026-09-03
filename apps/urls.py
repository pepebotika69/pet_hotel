from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from apps.auth.auth_views import csrf_token, login_view, logout_view, me, register
from apps.hotel.views.views import hotels

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("api/hotels", hotels),
    path("api/auth/csrf", csrf_token),
    path("api/auth/register", register),
    path("api/auth/login", login_view),
    path("api/auth/logout", logout_view),
    path("api/auth/me", me),
]
