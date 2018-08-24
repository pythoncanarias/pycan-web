import uuid
from decimal import Decimal

from django.db import models
from django.db.models import Max
from django.urls import reverse

from . import links
from events.models import Event


class TicketCategory(models.Model):
    # Twin, Early, Normal, ...
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

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

    class Meta:
        verbose_name_plural = 'ticket categories'


class Article(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name='articles'
    )
    category = models.ForeignKey(
        TicketCategory,
        on_delete=models.PROTECT,
        related_name='articles'
    )
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField()
    release_at = models.DateTimeField()

    def __str__(self):
        return self.price


class Ticket(models.Model):
    number = models.PositiveIntegerField(
        help_text='Consecutive number within event'
    )
    keycode = models.UUIDField(default=uuid.uuid4)
    customer_email = models.EmailField()
    sold_at = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=128, blank=True)
    article = models.ForeignKey(
        Article,
        on_delete=models.PROTECT,
        related_name='tickets'
    )
    customer_name = models.CharField(max_length=256, blank=True)
    customer_surname = models.CharField(max_length=256, blank=True)
    customer_phone = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return '{}/{} {}, {}'.format(
            self.number,
            self.ticket_type.event.title,
            self.surname,
            self.name,
        )

    def get_qrcode_url(self):
        return links.qr_code(self.pk)

    def get_absolute_url(self):
        return reverse('events:ticket_bought', args=(str(self.keycode),))
