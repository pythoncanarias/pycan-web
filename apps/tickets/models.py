#!/usr/bin/env python3

import io
import os
import random
import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils import timezone as dj_timezone
import pyqrcode

from . import links
from .constants import PAYMENT_METHOD
from .services.ticket_maker import TicketMaker
from utils.dates import just_today


class TicketCategory(models.Model):
    """Un evento puede tener distintos tipos de entrada.

    Este modelo permite crear esos tipos diferentes, que
    puedenn tener un nombre, slug y descripción propia.
    """
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
    HIDDEN = 'HIDDEN'

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
    release_at = models.DateTimeField(null=True, blank=True)
    participate_in_raffle = models.BooleanField(
        default=True,
        help_text=(
            'Indicates if people with this article'
            ' can be awarded in a potential raffle'
            ' at event'
            ),
        )

    @classmethod
    def load_article(cls, pk):
        """Returns an instance of the article.
        """
        try:
            return (
                cls.objects
                .select_related("event")
                .get(pk=pk)
                )
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return '{} [{}]'.format(self.category, self.event)

    def num_sold_tickets(self) -> int:
        """Return the total number of saled tickets.
        """
        return (
            self.tickets
            .exclude(refunded_at__isnull=False)
            .count()
            )

    def num_available_tickets(self):
        return self.stock - self.num_sold_tickets()

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

    def all_sold(self) -> bool:
        return self.num_available_tickets() <= 0

    def sale_ended(self) -> bool:
        return self.event.start_date < just_today()

    def status(self):
        if self.release_at is None:
            return Article.HIDDEN
        now = dj_timezone.now()
        if self.release_at > now:
            return Article.UPCOMING
        if self.all_sold() or self.sale_ended():
            return Article.SOLDOUT
        return Article.SALEABLE


class Ticket(models.Model):

    class Meta:
        ordering = ['sold_at']

    number = models.PositiveIntegerField(
        help_text=('Consecutive number within event '
                   '(if blank it will be automatically fulfilled)'),
        null=True,
        blank=True,
        )
    keycode = models.UUIDField(default=uuid.uuid4)
    sold_at = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=128, blank=True)
    payment_method = models.PositiveSmallIntegerField(
        choices=PAYMENT_METHOD.CHOICES,
        default=PAYMENT_METHOD.STRIPE,
        blank=True,
        null=True)
    article = models.ForeignKey(
        Article,
        on_delete=models.PROTECT,
        related_name='tickets'
    )
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=256, blank=True)
    customer_surname = models.CharField(max_length=256, blank=True)
    customer_phone = models.CharField(max_length=32, blank=True)
    send_at = models.DateTimeField(default=None, blank=True, null=True)
    refunded_at = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return '{}/{} [{}]'.format(
            self.number,
            self.article.event,
            self.customer_email
        )

    @property
    def event(self):
        return self.article.event

    @property
    def customer_full_name(self):
        return '{} {}'.format(self.customer_name, self.customer_surname)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.event.next_ticket_number()
        super().save(*args, **kwargs)

    def get_qrcode_url(self):
        return links.qr_code(self.pk)

    def get_absolute_url(self):
        return reverse('events:article_bought', args=(str(self.keycode),))

    def get_qrcode_as_svg(self, scale=8):
        img = pyqrcode.create(str(self.keycode))
        buff = io.BytesIO()
        img.svg(buff, scale=scale)
        return buff.getvalue().decode('ascii')

    @staticmethod
    def get_tickets_dir():
        _dir = os.path.join(settings.BASE_DIR, 'temporal', 'tickets')
        if not os.path.isdir(_dir):
            os.makedirs(_dir)
        return _dir

    def as_pdf(self, force=False):
        output_dir = Ticket.get_tickets_dir()
        pdf_file = f'ticket-{self.keycode}.pdf'
        full_name = os.path.join(output_dir, pdf_file)
        if not os.path.exists(full_name) or force:
            tm = TicketMaker(full_name, self)
            tm.create()
        return full_name


class Raffle(models.Model):

    class Meta:
        ordering = ['created_at']

    event = models.OneToOneField(
        'events.Event',
        related_name='raffle',
        on_delete=models.CASCADE,
        )
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Sorteo para {self.event}'

    def get_candidate_tickets(self):
        return self.event.all_tickets().filter(article__participate_in_raffle=True)

    def get_delivered_gifts(self):
        return self.gifts.filter(awarded_ticket__isnull=False)

    def get_undelivered_gifts(self):
        return self.gifts.filter(awarded_ticket__isnull=True)

    def get_awarded_tickets(self):
        return [
            gift.awarded_ticket
            for gift in self.gifts.filter(awarded_ticket__isnull=False)
        ]

    def get_unawarded_tickets(self):
        awarded_tickets_ids = [t.id for t in self.get_awarded_tickets()]
        candidate_tickets = self.get_candidate_tickets()
        return candidate_tickets.exclude(pk__in=awarded_tickets_ids)

    def get_missing_tickets(self):
        missing_tickets_ids = {
            missing_ticket.id
            for gift in self.gifts.all()
            for missing_ticket in gift.missing_tickets.all()
        }
        return Ticket.objects.filter(pk__in=missing_tickets_ids)

    def get_available_tickets(self):
        return self.get_unawarded_tickets().exclude(
            pk__in=self.get_missing_tickets())

    def get_random_ticket(self, with_replacement=False):
        if with_replacement:
            candidate_tickets = self.get_candidate_tickets()
        else:
            candidate_tickets = self.get_available_tickets()
        return random.choice(candidate_tickets)

    def clean_awarded_tickets(self):
        for gift in self.gifts.all():
            gift.awarded_ticket = None
            gift.awarded_at = None
            gift.missing_tickets.clear()
            gift.save()

    def get_absolute_url(self):
        return reverse('events:raffle', args=(self.event.slug,))

    @property
    def closed(self):
        return self.closed_at is not None

    @property
    def opened(self):
        return not self.closed


class Gift(models.Model):

    class Meta:
        ordering = ['name', 'description']

    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    raffle = models.ForeignKey(
        'tickets.Raffle',
        related_name='gifts',
        on_delete=models.CASCADE,
        )
    awarded_ticket = models.OneToOneField(
        'tickets.Ticket',
        related_name='gift',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        )
    awarded_at = models.DateTimeField(null=True, blank=True)
    missing_tickets = models.ManyToManyField(
        'tickets.Ticket',
        related_name='missing_gifts',
        )

    def __str__(self):
        return self.name

    def order(self) -> int:
        gifts_ids = list(
            Gift.objects
            .filter(raffle=self.raffle)
            .values_list('pk', flat=True)
            )
        return gifts_ids.index(self.id) + 1

    def awarded_ticket_for_display(self) -> str:
        return (
            f'{self.awarded_ticket.customer_full_name} '
            f'(#{self.awarded_ticket.number})'
            )
