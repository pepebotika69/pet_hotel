from django.urls import path

from apps.test_kafka.views import consume, produce

urlpatterns = [
    path("produce", produce),
    path("consume", consume),
]
