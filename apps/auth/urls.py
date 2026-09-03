from django.urls import path

from apps.auth.auth_views import csrf_token, login_view, logout_view, me, register

urlpatterns = [
    path("csrf", csrf_token),
    path("register", register),
    path("login", login_view),
    path("logout", logout_view),
    path("me", me),
]
