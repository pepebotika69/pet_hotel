from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods

from apps.embassy.forms.citizen_form import CitizenForm


@require_http_methods(["GET", "POST"])
def citizen_register(request):
    if request.method == "POST":
        form = CitizenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("citizen_register_success"))
    else:
        form = CitizenForm()

    return render(request, "embassy/citizen_register.html", {"form": form})


@require_GET
def citizen_register_success(request):
    return render(request, "embassy/citizen_register_success.html")
