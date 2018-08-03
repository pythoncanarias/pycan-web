import uuid
from decimal import Decimal
from django.db import models
from django.db.models import Max
from django.urls import reverse


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=150)
    title = models.CharField(max_length=220)
    active = models.BooleanField(default=False)
    start_date = models.DateField()

    def __str__(self):
        return self.title


class TicketType(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name='ticket_types',
        )
    name = models.CharField(max_length=80)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField()
    release_at = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def num_sold_tickets(self):
        return self.tickets.all().count()

    @property
    def num_available_tickets(self):
        return self.stock - self.tickets.all().count()

    @property
    def price_in_cents(self):
        return int(self.price * Decimal('100.0'))

    def next_number(self):
        data = self.tickets.aggregate(Max('number'))
        current_number = data.get('number__max', 0) or 0
        return current_number + 1

    def is_active(self):
        return (
            self.release_at is not None
            and self.release_at.date() < self.event.start_date
            )
    is_active.boolean = True


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    ticket_type = models.ForeignKey(
        TicketType,
        on_delete=models.PROTECT,
        related_name='tickets',
        )
    number = models.PositiveIntegerField()
    keycode = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=48)
    surname = models.CharField(max_length=72)
    email = models.CharField(max_length=260)
    phone = models.CharField(max_length=14, blank=True)
    sold_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}/{} {}, {}'.format(
            self.number,
            self.ticket_type.event.title,
            self.surname,
            self.name,
            )

    def get_qrcode_url(self):


    def get_absolute_url(self):
        return reverse('events:ticket_bought', args=(str(self.keycode),))
