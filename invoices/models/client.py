from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)

    nif = models.CharField(max_length=12)

    address = models.CharField(max_length=120)
    rest_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=30)

    def __str__(self):
        return '{} nif: {}'.format(self.name, self.nif)
