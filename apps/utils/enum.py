from enum import StrEnum as StrEnumLib


class StrEnum(StrEnumLib):
    @classmethod
    def get_choices(cls):
        return [(x.value, x.value) for x in cls]

    @classmethod
    def get_values(cls):
        return [x.value for x in cls]