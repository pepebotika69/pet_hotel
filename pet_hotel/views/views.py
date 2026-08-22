from django.http import JsonResponse
from django.views.decorators.http import require_GET

from pet_hotel.views.decorators import login_required_json


@login_required_json
@require_GET
def hotels(request):
    return JsonResponse({
        "hotels": [
            {"title": "title 1"},
            {"title": "title 2"},
            {"title": "title 3"},
            {"title": "title 4"},
        ]
    })
