from django.urls import path

from apps.embassy.views.citizen_register import citizen_register, citizen_register_success

urlpatterns = [
    path("embassy/citizen/register/", citizen_register, name="citizen_register"),
    path("embassy/citizen/register/success/", citizen_register_success, name="citizen_register_success"),
]
