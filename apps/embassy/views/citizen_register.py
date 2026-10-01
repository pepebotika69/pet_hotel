from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods

from apps.embassy.forms.citizen_form import CitizenForm
from apps.embassy.models.registration_token import RegistrationToken


@require_http_methods(["GET", "POST"])
def citizen_register(request, token):
    try:
        reg_token = RegistrationToken.objects.get(token=token)
    except RegistrationToken.DoesNotExist:
        return render(request, "embassy/citizen_register_invalid.html", {"reason": "invalid"})

    if reg_token.is_used:
        return render(request, "embassy/citizen_register_invalid.html", {"reason": "used"})

    if reg_token.is_expired:
        return render(request, "embassy/citizen_register_invalid.html", {"reason": "expired"})

    if request.method == "POST":
        form = CitizenForm(request.POST)
        if form.is_valid():
            form.save()
            reg_token.used_at = timezone.now()
            reg_token.save(update_fields=["used_at"])
            return redirect(reverse("citizen_register_success"))
    else:
        form = CitizenForm()

    return render(request, "embassy/citizen_register.html", {"form": form, "token": token})


@require_GET
def citizen_register_success(request):
    return render(request, "embassy/citizen_register_success.html")
