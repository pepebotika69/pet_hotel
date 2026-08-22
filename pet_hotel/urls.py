from django.contrib import admin
from django.urls import path

from pet_hotel.views.auth_views import csrf_token, register, login_view, logout_view, me
from pet_hotel.views.views import hotels

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hotels', hotels),
    path('api/auth/csrf', csrf_token),
    path('api/auth/register', register),
    path('api/auth/login', login_view),
    path('api/auth/logout', logout_view),
    path('api/auth/me', me),
]
