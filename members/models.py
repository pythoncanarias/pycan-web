from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from pytz import utc

MSG_PUBLIC_MEMBERSHIP = "Si está activo, tu perfil de usuario se mostrará" \
                        " públicamente en la web"

MSG_STATUS_ID_CODE = "NIF para españoles o NIE si procede"


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    email = models.EmailField(
        max_length=300,
        unique=True,
        default='info@pythoncanarias.es'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    member_until = models.DateTimeField(auto_now_add=True)

    address = models.CharField(max_length=100, blank=True)
    rest_address = models.CharField(max_length=100, blank=True)
    po_box = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=20, blank=True)
    public_membership = models.BooleanField(
        default=False,
        help_text=MSG_PUBLIC_MEMBERSHIP,
    )
    phone = models.CharField(max_length=32, default=None, blank=True)
    state_id_code = models.CharField(
        max_length=22,
        default=None,
        blank=True,
        help_text=MSG_STATUS_ID_CODE,
    )
    stripe_customer_id = models.CharField(
        max_length=64,
        default=None,
        blank=True,
    )

    @property
    def full_name(self):
        return f'{self.user.last_name}, {self.user.first_name}'

    @property
    def active(self):
        return datetime.now(tz=utc) < self.member_until

    def __str__(self):
        return (f'{self.user.first_name} {self.user.last_name} '
                f'member until {self.member_until}')
