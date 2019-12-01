import datetime

from django.contrib.auth.models import User
from django.db import models

from .constants import (FEE_AMOUNT, FEE_PAYMENT_TYPE, MEMBER_CATEGORY,
                        MEMBER_POSITION, DEFAULT_MEMBERSHIP_PERIOD)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=100, blank=True)
    rest_address = models.CharField(max_length=100, blank=True)
    po_box = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def email(self):
        return self.user.email

    @property
    def member_id(self):
        return self.id

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ('id', 'user__first_name', 'user__last_name')


class Position(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    position = models.CharField(max_length=3, choices=MEMBER_POSITION.CHOICES)
    since = models.DateField()
    until = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        created = not self.id
        super().save(*args, **kwargs)

        if created and self.active:
            Position.objects.filter(active=True,
                                    position=self.position).exclude(
                                        id=self.id).update(until=self.since,
                                                           active=False)

    def __str__(self):
        return f'{self.member.full_name} as {self.position}'

    class Meta:
        ordering = ('since', 'position', 'member')


class Membership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    member_category = models.CharField(max_length=1,
                                       choices=MEMBER_CATEGORY.CHOICES,
                                       default=MEMBER_CATEGORY.NUMBER)
    valid_from = models.DateField()
    valid_until = models.DateField(blank=True, null=True)
    fee_received_at = models.DateTimeField(blank=True, null=True)
    fee_amount = models.IntegerField(choices=FEE_AMOUNT.CHOICES,
                                     default=FEE_AMOUNT.GENERAL)
    fee_payment_type = models.CharField(
        max_length=2,
        choices=FEE_PAYMENT_TYPE.CHOICES,
        default=FEE_PAYMENT_TYPE.BANK_TRANSFERENCE,
        blank=True)
    fee_payment_reference = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f'{self.member.full_name} from {self.valid_from}'

    class Meta:
        ordering = ('valid_from', 'member')

    def save(self, *args, **kwargs):
        if (self.fee_amount != FEE_AMOUNT.EXEMPT
                and self.valid_until is None):
            self.valid_until = self.valid_from + datetime.timedelta(
                days=DEFAULT_MEMBERSHIP_PERIOD)
        super().save(args, kwargs)
