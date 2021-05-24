from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)

    nif = models.CharField(max_length=12)

    address = models.CharField(max_length=120)
    rest_address = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=30)

    email = models.EmailField(max_length=150, blank=True, null=True)

    def __str__(self):
        return '{} nif: {}'.format(self.name, self.nif)
