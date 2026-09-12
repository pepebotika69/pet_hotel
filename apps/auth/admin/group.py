from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.auth.admin.constants import GROUP_PREFIX_MAP

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    def _allowed_prefixes(self, user):
        user_group_names = set(user.groups.values_list("name", flat=True))
        return [prefix for gname, prefix in GROUP_PREFIX_MAP.items() if gname in user_group_names]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        prefixes = self._allowed_prefixes(request.user)
        if not prefixes:
            return qs.none()
        q = Q()
        for prefix in prefixes:
            q |= Q(name__startswith=prefix)
        return qs.filter(q)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            allowed_prefixes = self._allowed_prefixes(request.user)

            def validate_name(value):
                if not any(value.startswith(p) for p in allowed_prefixes):
                    raise ValidationError(
                        _("Group name must start with one of: %(prefixes)s"),
                        params={"prefixes": ", ".join(allowed_prefixes)},
                    )

            form.base_fields["name"].validators.append(validate_name)
        return form
