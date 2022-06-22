from django.core.exceptions import ObjectDoesNotExist

from .models import Label


class LabelConverter:
    regex = '[-a-zA-Z0-9_]+'

    def to_python(self, value: str) -> Label:
        try:
            return Label.objects.get(slug=value)
        except ObjectDoesNotExist as err:
            raise ValueError('This label does not exist!') from err

    def to_url(self, value: Label) -> str:
        return value.slug
