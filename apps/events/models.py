import datetime
import locale
import os
import uuid
from functools import partial

from colorfield.fields import ColorField
from django.conf import settings
from django.db import models
from django.db.models import Max
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont

from apps.events import links
from apps.locations.models import Venue
from apps.organizations.models import OrganizationRole
from apps.schedule.models import Track
from apps.speakers.models import Speaker
from apps.tickets.models import Ticket

from . import time_utils


class Event(models.Model):
    class Meta:
        ordering = ["-start_date"]

    name = models.CharField(max_length=256)
    hashtag = models.SlugField(unique=True)
    active = models.BooleanField(
        help_text="The current event is shown in the events page",
        default=False,
        )
    opened_ticket_sales = models.BooleanField(default=False)
    start_date = models.DateField()
    venue = models.ForeignKey(
        Venue,
        related_name="events",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        )
    # 50 minutes as default duration for each slot
    default_slot_duration = models.DurationField(default=50 * 60)
    short_description = models.TextField(
        blank=True,
        help_text="Shown in events list",
    )
    description = models.TextField(
        blank=True,
        help_text="Shown in main page of event (markdown allowed)",
    )
    cover = models.ImageField(
        upload_to="events/event/",
        blank=True,
        help_text="Should be squared (250x250 max). Shown in events list.",
    )
    poster = models.FileField(
        upload_to="events/event/",
        blank=True,
    )
    sponsorship_brochure = models.FileField(
        upload_to="events/event/",
        blank=True,
    )
    hero = models.ImageField(
        upload_to="events/event/",
        blank=True,
        help_text="Enough 1200px wide. Shown shaded in main page of event",
    )
    external_tickets_url = models.URLField(
        blank=True,
        help_text="Should be filled if tickets are sold outside our site",
    )
    closed_schedule = models.BooleanField(default=False)
    # Call for papers fields
    cfp_start_at = models.DateTimeField(
        blank=True,
        default=None,
        null=True,
        help_text="First day of Call for Papers period",
    )
    cfp_stop_at = models.DateTimeField(
        blank=True,
        default=None,
        null=True,
        help_text="End of Call for Papers period (This day is not included)",
    )

    def call_for_paper_is_open(self) -> bool:
        """Returns True if it's possible to present a proposal for the event
        """
        if self.cfp_start_at is None:
            return False
        now = timezone.now()
        if self.cfp_stop_at is None:
            return self.cfp_start_at <= now
        return self.cfp_start_at <= now < self.cfp_stop_at

    def __str__(self):
        return self.name

    @property
    def slug(self):
        return self.hashtag.lower()

    def end_datetime(self):
        try:
            return self.schedule.order_by("end").last().end
        except AttributeError:
            end_time = datetime.time(23, 59, 59, tzinfo=timezone.get_current_timezone())
            return datetime.datetime.combine(self.start_date, end_time)

    def get_google_calendar_url(self):
        start_datetime = self.start_datetime().strftime("%Y%m%dT%H%M%SZ")
        end_datetime = self.end_datetime().strftime("%Y%m%dT%H%M%SZ")
        return f"https://www.google.com/calendar/render?action=TEMPLATE&text={self.name}&details={self.description}&location={self.venue}&dates={start_datetime}%2F{end_datetime}"

    @classmethod
    def get_by_slug(cls, slug):
        return cls.objects.get(hashtag__iexact=slug)

    def get_full_url(self):
        return "http://{}{}".format(
            settings.DOMAIN,
            links.event_detail(self.slug),
        )

    def get_long_start_date(self, to_locale=settings.LC_TIME_SPANISH_LOCALE):
        locale.setlocale(locale.LC_TIME, to_locale)
        return self.start_date.strftime("%A %d de %B de %Y").capitalize()

    def speakers(self):
        speaker_ids = self.schedule.values_list("speakers").distinct()
        return Speaker.objects.filter(pk__in=speaker_ids).order_by("name", "surname")

    def organization_roles(self):
        org_roles_ids = self.memberships.values_list("category__role").distinct()
        return OrganizationRole.objects.filter(pk__in=org_roles_ids).order_by(
            "order", "name"
        )

    def memberships_for_display(self):
        result = {}
        for role in self.organization_roles():
            r = {}
            for cat in role.organization_categories.order_by("order", "name"):
                orgs = cat.organizations(self)
                # insert joint organizations next to its reference
                for i, org in enumerate(orgs):
                    for jorg in reversed(org.joint_organizations()):
                        orgs.insert(i + 1, jorg)
                if orgs:
                    r[cat] = orgs
            if r:
                result[role] = r
        return result

    def tracks(self):
        tracks_ids = self.schedule.values_list("track").distinct()
        return Track.objects.filter(pk__in=tracks_ids).order_by("order", "name")

    def plenary_scheduled_items(self):
        return self.schedule.filter(track__isnull=True).order_by("start")

    def start_datetime(self):
        try:
            return self.schedule.order_by("start").first().start
        except AttributeError:
            start_time = datetime.time(0, 0, 0, tzinfo=timezone.get_current_timezone())
            return datetime.datetime.combine(self.start_date, start_time)

    @property
    def start_hour(self):
        return time_utils.as_hour(self.start_datetime())

    def _scheduled_items_for_display(self, start=None, end=None):
        result = {"type": "scheduled_items", "tracks": []}
        exist_scheduled_item = False
        for track in self.tracks():
            scheduled_items = track.schedule_in_range(start, end, event=self)
            if scheduled_items:
                exist_scheduled_item = True
            result["tracks"].append(
                {"track": track, "scheduled_items": scheduled_items}
            )
        if not exist_scheduled_item:
            result = None
        return result

    def schedule_for_display(self):
        tracks = self.tracks()
        result = []
        if tracks:
            if len(tracks) > 1:
                result.append({"type": "tracks", "tracks": tracks})
            start, end = self.start_datetime(), None
            for psi in list(self.plenary_scheduled_items()):
                end = psi.start
                scheduled_items = self._scheduled_items_for_display(start, end)
                if scheduled_items:
                    result.append(scheduled_items)
                result.append({"type": "plenary_scheduled_item", "schedule": psi})
                start, end = psi.end, None

            scheduled_items = self._scheduled_items_for_display(start, end)
            if scheduled_items:
                result.append(scheduled_items)
        return result

    def get_non_org_speakers(self):
        speakers_ids = (
            self.schedule.all()
            .exclude(slot__category__code="organizing")
            .values_list("speakers", flat=True)
        )
        return Speaker.objects.filter(pk__in=speakers_ids).order_by("name", "surname")

    def all_tickets(self):
        """Get all the tickets sold for a particular event.

        Returns a queryset of tickets, with select related
        articles preloaded.
        """
        qs = Ticket.objects.select_related("article")
        qs = qs.filter(article__event=self)
        return qs

    def all_articles(self):
        """Get all the articles we can sold for a particular event.

        Returns a queryset of articles, with select related
        categorias preloaded, ordered by name.
        """
        qs = self.articles.select_related("category")
        qs = qs.order_by("category__name")
        return qs

    def num_sold_tickets(self):
        return sum([a.num_sold_tickets for a in self.articles.all()])

    def num_available_tickets(self):
        return sum([a.num_available_tickets for a in self.articles.all()])

    def next_ticket_number(self):
        """Get the number for the next ticket within this event."""
        data = self.all_tickets().aggregate(Max("number"))
        current_number = data.get("number__max", 0) or 0
        return current_number + 1

    @property
    def qualified_hashtag(self):
        return f"#{self.hashtag}"

    @property
    def twitter_hashtag_url(self):
        return f"https://twitter.com/hashtag/{self.slug}?f=live"

    def render_all_badges(self, pdf_only=False, remove_badges=True):
        """
        Render all Badges for this event as images, save them and make an
        unique PDF with all
        badges for printing.
        :param pdf_only: If True, it won't render the intermediate badges,
        only the final PDF with all the images in the folder.
        :param remove_badges: If True, remove the intermediate badges to keep
        the server clean.
        :return:
        """
        badge = self.badge_set.first()
        if not pdf_only:
            for ticket in self.all_tickets():
                badge.render(ticket)
        image_dir = os.path.join(settings.MEDIA_ROOT, f"events/{self.slug}/")
        image_list = os.listdir(image_dir)
        badges = [
            Image.open(os.path.join(image_dir, img)).convert("RGB")
            for img in image_list
            if img.split(".")[1] != "pdf"
        ]
        if len(badges) == 0:
            return
        # Calculate the size of the page (A4) depending on the base image dpi.
        dpi = Image.open(badge.base_image.path).info.get("dpi")
        if not dpi:
            print(("There was an error getting the DPI from the badge. " "Aborting"))
            raise KeyError
        pdf_pages = []
        offset_top = 50
        offset_side = 10
        x = offset_side
        y = offset_top

        a4_width = int(210 / 25.4 * dpi[0])
        a4_height = int(297 / 25.4 * dpi[1])
        # PDF blank page
        current = Image.new("RGB", (a4_width, a4_height), (255, 255, 255))
        pdf_pages.append(current)
        for img in badges:
            width, height = img.size
            if current is None or y + height >= a4_height:
                # Create a new PDF page and reset x, y
                if current not in pdf_pages:
                    pdf_pages.append(current)
                x = offset_side
                y = offset_top
                current = Image.new("RGB", (a4_width, a4_height), (255, 255, 255))
            current.paste(img, (x, y))
            if x + (width * 2) >= a4_width:  # No more badges in the row
                x = offset_side
                y += height
            else:
                x += width
        pdf = Image.new("RGB", (a4_width, a4_height), (255, 255, 255))
        pdf_output = os.path.join(image_dir, "print.pdf")
        pdf.save(
            pdf_output,
            "PDF",
            resolution=100.0,
            save_all=True,
            quality=100,
            append_images=pdf_pages,
        )
        del badges
        if remove_badges:
            for img in image_list:
                if img.split(".")[1] != "pdf":
                    os.remove(os.path.join(image_dir, img))
        return f"{settings.MEDIA_URL}events/{self.slug}/print.pdf"


class Badge(models.Model):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    base_image = models.ImageField(upload_to="events/badges/", blank=False)
    # Coordinates start from the top-left corner
    name_coordinates = models.CharField(
        max_length=255,
        verbose_name="Person name coordinates (eg 15,23).",
        default="0,0",
    )
    name_font_size = models.PositiveIntegerField(default=24)
    name_color = ColorField(default="#FFFFFF")
    number_coordinates = models.CharField(
        max_length=255, verbose_name="Ticket number coordinates", default="0,0"
    )
    number_font_size = models.PositiveIntegerField(default=24)
    number_color = ColorField(default="#FFFFFF")
    category_coordinates = models.CharField(
        max_length=255, verbose_name="Ticket category coordinates", default="0,0"
    )
    category_font_size = models.PositiveIntegerField(default=24)
    category_color = ColorField(default="#FFFFFF")

    def __str__(self):
        return f"Badge for {self.event.name}"

    @staticmethod
    def coord_to_tuple(coord):
        return tuple(int(i) for i in coord.split(","))

    @staticmethod
    def _parse_name(name: str, surname: str):
        name_list = name.split()
        if len(name_list) >= 2 and len(name_list[1]) > 2:
            name = f"{name_list[0]} {name_list[1][:1]}."

        return f"{name} \n{surname}"

    @staticmethod
    def _hex_to_rgb(color: str) -> tuple:
        return tuple(int(color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))

    def add_field(
        self, image_draw: ImageDraw, text: str, coord: str, font_size: int, color: str
    ):
        font = ImageFont.truetype("fonts/arial.ttf", size=font_size)
        image_draw.text(
            self.coord_to_tuple(coord), text, fill=self._hex_to_rgb(color), font=font
        )
        return image_draw

    def render(self, ticket: Ticket):
        img = Image.open(self.base_image.path)
        image_draw = ImageDraw.Draw(img)
        self.add_field(
            image_draw,
            self._parse_name(ticket.customer_name, ticket.customer_surname),
            self.name_coordinates,
            self.name_font_size,
            self.name_color,
        )
        self.add_field(
            image_draw,
            str(ticket.number),
            self.number_coordinates,
            self.number_font_size,
            self.number_color,
        )
        self.add_field(
            image_draw,
            ticket.article.category.name,
            self.category_coordinates,
            self.category_font_size,
            self.category_color,
        )
        # test
        path = (
            f"{settings.MEDIA_ROOT}/events/{self.event.slug}/"
            "badge_{ticket.number}.png"
        )
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError:
                raise
        img.save(path, quality=100)
        return img


# Waiting List


class WaitingList(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    phone = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    fixed_at = models.DateTimeField(default=None, blank=True, null=True)
    buy_code = models.UUIDField(default=uuid.uuid4, unique=True)

    @classmethod
    def load_by_buy_code(cls, buy_code):
        try:
            return cls.objects.get(buy_code=buy_code)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        if self.fixed_at:
            return "{}, {} ({}) FIXED".format(
                self.surname,
                self.name,
                self.email,
            )
        else:
            return "{}, {} ({}) waiting since {}".format(
                self.surname,
                self.name,
                self.email,
                self.created_at,
            )


# Refunds
class Refund(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    fixed_at = models.DateTimeField(default=None, blank=True, null=True)
    sell_code = models.UUIDField(default=uuid.uuid4)

    @classmethod
    def load_by_sell_code(cls, sell_code):
        try:
            return cls.objects.get(sell_code=sell_code)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        if self.fixed_at:
            return "Refund for ticket {} [FIXED]".format(self.ticket)
        else:
            return "Refund for ticket {}".format(self.ticket)

    def get_absolute_url(self):
        return links.refund_accepted(self.event.slug, self.pk)

    def get_position(self):
        return (
            Refund.objects.all()
            .filter(event=self.event)
            .filter(fixed_at__isnull=True)
            .filter(created_at__lt=self.created_at)
            .count()
            + 1
        )

    @classmethod
    def exists(cls, event, ticket):
        return cls.objects.filter(event=event, ticket=ticket).count() > 0


# Trade class (intermedite between WaitingList and Refund)


class Trade(models.Model):

    TERM_IN_HOURS = 3

    sell_code = models.UUIDField(default=uuid.uuid4, unique=True)
    buy_code = models.UUIDField(default=uuid.uuid4, unique=True)
    start_at = models.DateTimeField(default=time_utils.now)
    finish_at = models.DateTimeField(
        default=partial(time_utils.now_plus, hours=TERM_IN_HOURS)
    )
    fixed_at = models.DateTimeField(default=None, blank=True, null=True)
    finished = models.BooleanField(default=False)
    sucessful = models.BooleanField(default=False)

    @classmethod
    def load_active_trade(cls):
        qs = cls.objects.filter(finished=False)
        num_trades = qs.count()
        assert num_trades in (0, 1)
        return qs.first() if num_trades == 1 else None

    def finish(self, sucessful=False):
        if not self.finished:
            now = time_utils.now()
            self.finished = True
            self.finish_at = now
            if sucessful:
                self.sucessful = True
                self.fixed_at = now
            self.save()

    def is_due(self):
        if not self.finished and time_utils.now() > self.finish_at:
            self.finish(sucessful=False)
        return self.finished


class Proposal(models.Model):
    event = models.ForeignKey(
        Event,
        related_name="proposals",
        on_delete=models.PROTECT,
    )
    name = models.CharField(max_length=256, verbose_name="Nombre")
    surname = models.CharField(max_length=256, verbose_name="Apellidos")
    email = models.EmailField(blank=True, verbose_name="Email")
    title = models.CharField(max_length=340, verbose_name="Título")
    description = models.TextField(
        verbose_name="Descripción",
        help_text=("Cuéntamos en dos o tres párrafos tu propuesta de charla.")
    )
    presented_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} por {self.name} {self.surname}"
