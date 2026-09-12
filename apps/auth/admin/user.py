from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from apps.auth.admin.constants import GROUP_PREFIX_MAP

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        user_group_names = set(request.user.groups.values_list("name", flat=True))
        allowed_groups = [gname for gname in GROUP_PREFIX_MAP if gname in user_group_names]
        if not allowed_groups:
            return qs.none()
        return qs.filter(groups__name__in=allowed_groups).distinct()
