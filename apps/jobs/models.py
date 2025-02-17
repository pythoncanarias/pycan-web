import datetime
import urllib
from functools import partial

from django.db import models
from django.urls import reverse

from apps.commons.filters import date_from_now
from apps.commons.twitter import Twitter
from apps.organizations.models import Organization

# Create your models here.

CONTRACT_TYPES = [
    ("IND", "Indefinido"),
    (
        "Temporal",
        [
            ("TEV", "Eventual"),
            ("TOS", "Por obras y servicios"),
            ("TDI", "De interinidad"),
            ("TDR", "De relevo"),
        ],
    ),
    ("DFA", "De formación y aprendizaje"),
    ("DPR", "De prácticas"),
    ("OTR", "Otro"),
]

WORK_MODES = [
    ("RM", "Remoto"),
    ("PR", "Presencial"),
    ("MX", "Mixto Remoto/Presencial"),
    ("NA", "Sin determinar / Desconocido"),
]


class ActiveJobOfferManager(models.Manager):
    def get_queryset(self):
        today = datetime.date.today()
        return super().get_queryset().filter(approved=True).filter(valid_until__gte=today)


class JobOffer(models.Model):
    objects = models.Manager()  # The default manager.
    actives = ActiveJobOfferManager()  # Only the active jobs offer

    class Meta:
        db_table = "job_offer"
        verbose_name = "Oferta de trabajo"
        verbose_name_plural = "Ofertas de trabajo"

    employer = models.CharField("Ofertante", max_length=120)
    title = models.CharField("Nombre del puesto", max_length=220)
    description = models.TextField("Texto de la oferta", max_length=2000)
    salary = models.CharField("Salario o rango salarial", max_length=80, blank=True)
    contract_type = models.CharField(
        "Tipo de contrato",
        max_length=3,
        choices=CONTRACT_TYPES,
        default="IND",
    )
    work_mode = models.CharField(
        "Remoto/Presencial",
        max_length=2,
        choices=WORK_MODES,
    )
    part_time = models.BooleanField("A tiempo parcial", default=False)
    more_info = models.URLField(
        "Enlace para más información",
        max_length=250,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateField(
        "Válido hasta",
        blank=True,
        default=partial(date_from_now, days=91),
    )
    approved = models.BooleanField("Aprobada", default=False)

    def __str__(self):
        if self.employer and self.employer.upper() != 'N/A':
            return "{} en {}".format(
                self.title,
                self.employer,
            )
        else:
            return self.title

    def is_valid(self):
        return self.approved and datetime.date.today() <= self.valid_until

    def get_full_url(self):
        path = reverse('jobs:index') + f'#job{self.pk}'
        organization = Organization.load_main_organization()
        return urllib.parse.urljoin(organization.url, path)

    def save(self, *args, **kwargs):
        already_exists = self.pk is not None
        super().save(*args, **kwargs)
        ''' tweepy.error.TweepError: [{'message': 'You currently have access to a subset of Twitter API v2 endpoints and limited v1.1 endpoints (e.g. media post, oauth) only. If you need access to this endpoint, you may need a different access level. You can learn more here: https://developer.twitter.com/en/portal/product', 'code': 453}]
        if not already_exists and self.approved:
            t = Twitter()
            msg = f'💼  Oferta de empleo: {self} {self.get_full_url()}'
            t.post(msg)'''
