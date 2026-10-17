from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.auth.admin.constants import GROUP_PREFIX_MAP
from apps.auth.admin.logic.user import send_login_after_registration_email

admin.site.unregister(User)


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreateForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_group_names = set(request.user.groups.values_list("name", flat=True))
        allowed_groups = [gname for gname in GROUP_PREFIX_MAP if gname in user_group_names]
        if not allowed_groups:
            return qs.none()
        return qs.filter(groups__name__in=allowed_groups).distinct()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change and obj.email:
            warning = send_login_after_registration_email(obj)
            if warning:
                self.message_user(request, warning, messages.WARNING)
