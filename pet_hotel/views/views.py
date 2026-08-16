from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def check(request):
    return JsonResponse({
        "title": "hello world"
    })


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
