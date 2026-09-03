from django.urls import path

from apps.hotel.views.views import hotels

urlpatterns = [
    path("hotels", hotels),
]
