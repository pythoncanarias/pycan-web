import uuid
from decimal import Decimal
from PIL import ImageFont, ImageDraw, Image

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
        if self.release_at is None:
            return Article.HIDDEN
        now = django.utils.timezone.now()
        if self.release_at > now:
            return Article.UPCOMING
        today = now.date()
        if self.num_available_tickets <= 0 or self.event.start_date < today:
            return Article.SOLDOUT
        return Article.SALEABLE


class Ticket(models.Model):
    number = models.PositiveIntegerField(
        help_text=('Consecutive number within event '
                   '(if blank it will be automatically fulfilled)'),
        null=True,
        blank=True)
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
    send_at = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return '{}/{} [{}]'.format(
            self.number,
            self.article.event,
            self.customer_email
        )

    @property
    def event(self):
        return self.article.event

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.event.next_ticket_number()
        super().save(*args, **kwargs)

    def get_qrcode_url(self):
        return links.qr_code(self.pk)

    def get_absolute_url(self):
        return reverse('events:article_bought', args=(str(self.keycode),))


class Badge(models.Model):
    article = models.ForeignKey('tickets.Article', on_delete=models.CASCADE)
    base_image = models.ImageField(upload_to=f"events/badges/", blank=False)
    # Coordinates start from the top-left corner
    name_coordinates = models.CharField(
        max_length=255,
        verbose_name="eg: 100,50 (0,0 will prevent this field to be printed)"
    )
    name_font_size = models.PositiveIntegerField()
    #name_color = ""
    number_coordinates = models.CharField(
        max_length=255,
        verbose_name="eg: 100,50 (0,0 will prevent this field to be printed)"
    )
    number_font_size = models.PositiveIntegerField()
    #number_color = ""
    category_coordinates = models.CharField(
        max_length=255,
        verbose_name="eg: 100,50 (0,0 will prevent this field to be printed)"
    )
    category_font_size = models.PositiveIntegerField()
    #category_color = ""

    @staticmethod
    def coord_to_tuple(coord):
        return tuple(int(i) for i in coord.split(","))

    def __str__(self):
        return f'Badge for {self.article}'

    def render(self, ticket=Ticket):
        img = Image.open(self.base_image.path)
        image_draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("fonts/arial.ttf", size=20)
        print(f"Rendering ticket {ticket.number} for {ticket.customer_name} on {self.coord_to_tuple(self.name_coordinates)} using base image = {self.base_image.path}")
        image_draw.text(
            self.coord_to_tuple(self.name_coordinates),
            f'{ticket.customer_name} \n{ticket.customer_surname}',
            fill=(255, 255, 255),
            font=font
        )
        # test
        img.save(f"image_{ticket.customer_name}.png", quality=100)
        return img
