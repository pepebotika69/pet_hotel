from enum import StrEnum as StrEnumLib

from django.utils.translation import gettext_lazy as _


class StrEnum(StrEnumLib):
    @classmethod
    def get_choices(cls):
        return [(x.value, _(x.value)) for x in cls]

    @classmethod
    def get_values(cls):
        return [x.value for x in cls]
