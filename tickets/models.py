import uuid
from decimal import Decimal

import django

from django.db import models
from django.db.models import Max
from django.urls import reverse

from . import links


class TicketCategory(models.Model):
    # Twin, Early, Normal, ...

    class Meta:
        verbose_name_plural = 'ticket categories'

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def image(self):
        return {
            'url': 'events/img/ticket-{}.png'.format(self.slug),
            'width': 222,
            'height': 64,
        }


class Article(models.Model):

    SOLDOUT = 'SOLDOUT'
    SALEABLE = 'SALEABLE'
    UPCOMING = 'UPCOMING'

    event = models.ForeignKey(
        'events.Event',
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
        return '{} [{}]'.format(self.category, self.event)

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
        return self.status() == Article.SALEABLE
    is_active.boolean = True

    def status(self):
        now = django.utils.timezone.now()
        if self.release_at is None or self.release_at > now:
            return Article.UPCOMING
        today = now.date()
        if self.num_available_tickets <= 0 or self.event.start_date < today:
            return Article.SOLDOUT
        return Article.SALEABLE


class Ticket(models.Model):
    number = models.PositiveIntegerField(
        help_text='Consecutive number within event'
    )
    keycode = models.UUIDField(default=uuid.uuid4)
    sold_at = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=128, blank=True)
    article = models.ForeignKey(
        Article,
        on_delete=models.PROTECT,
        related_name='tickets'
    )
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=256, blank=True)
    customer_surname = models.CharField(max_length=256, blank=True)
    customer_phone = models.CharField(max_length=32, blank=True)
    send_at = models.DateTimeField(defaut=None)

    def __str__(self):
        return '{}/{} [{}]'.format(
            self.number,
            self.article.event,
            self.customer_email
        )

    def get_qrcode_url(self):
        return links.qr_code(self.pk)

    def get_absolute_url(self):
        return reverse('events:article_bought', args=(str(self.keycode),))
