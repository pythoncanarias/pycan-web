from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    created_on = models.DateTimeField(auto_now_add=True)
    member_until = models.DateTimeField(auto_now_add=True)

    address = models.CharField(max_length=100, blank=True, null=True)
    rest_address = models.CharField(max_length=100, blank=True, null=True)
    po_box = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} member until {self.member_until}'
