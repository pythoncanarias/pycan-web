from django.db import models


class Concept(models.Model):
    description = models.CharField(max_length=120)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    invoice = models.ForeignKey('invoices.Invoice', on_delete=models.CASCADE)

    def __str__(self):
        return self.description
