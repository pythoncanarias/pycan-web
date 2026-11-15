from datetime import date as Date
from datetime import timedelta as TimeDelta
from calendar import isleap

from django.contrib.auth import get_user_model
from django.db import models
from django.db import transaction
from django.db.models import OuterRef, Subquery
from django.utils import timezone

from utils.security import generate_pronunciable_password
from .constants import (
    DEFAULT_MEMBERSHIP_PERIOD,
    DEFAULT_POSITION_PERIOD,
    FEE_AMOUNT,
    FEE_PAYMENT_TYPE,
    MEMBER_POSITION,
)

User = get_user_model()


class MemberManager(models.Manager):

    def get_queryset(self):
        last_membership = (
            Membership.objects
            .filter(member=OuterRef("pk"))
            .order_by('-valid_until')
            )
        return (
            super().get_queryset()
            .select_related('user')
            .prefetch_related('membership_set')
            .annotate(
                valid_until=Subquery(last_membership.values('valid_until')[:1])
                )
            )

    def actives(self):
        now = timezone.now()
        return self.get_queryset().filter(valid_until__gte=now)


class Member(models.Model):

    class Meta:
        ordering = ('id', 'user__first_name', 'user__last_name')
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=100, blank=True)
    rest_address = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_founder = models.BooleanField(default=False)
    is_honorary = models.BooleanField(default=False)
    remarks = models.CharField(max_length=512, blank=True)
    email = models.EmailField(
        max_length=320,
        unique=True,
        blank=False,
        )

    objects = MemberManager()

    @classmethod
    def load_from_username(cls, username):
        try:
            member = cls.objects.get(user__username=username)
            return member
        except cls.DoesNotExist:
            return None

    @classmethod
    def load_from_email(cls, email):
        rq = cls.objects.select_related('user')
        try:
            member = rq.get(email=email)
            return member
        except (cls.DoesNotExist, cls.MultipleObjectsReturned):
            return None

    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def member_id(self):
        return self.id

    def __str__(self):
        return self.full_name

    @property
    def active(self) -> bool:
        """Verdadero si el socio/a está activo/a a la fecha actual.
        """
        if self.valid_until:
            now = timezone.now().date()
            return now <= self.valid_until
        return False


class PositionManager(models.Manager):

    def actives(self):
        return (
            super().get_queryset()
            .select_related('member__user')
            .exclude(until__lt=timezone.now().date())
            )


class Position(models.Model):

    class Meta:
        ordering = ('since', 'position', 'member')
        verbose_name = 'Junta de gobierno'

    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    position = models.CharField(max_length=3, choices=MEMBER_POSITION.CHOICES)
    since = models.DateField()
    until = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=512, blank=True)

    objects = PositionManager()

    def save(self, *args, **kwargs):
        created = not self.id
        if self.until is None:
            self.until = self.since + DEFAULT_POSITION_PERIOD
        super().save(*args, **kwargs)
        if created:
            Position.objects.filter(position=self.position).exclude(
                id=self.id
            ).update(until=self.since)

    def __str__(self):
        return f'{self.member.full_name} as {self.position}'

    @property
    def active(self):
        return self.until is None or timezone.now().date() <= self.until


class Membership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    valid_from = models.DateField()
    valid_until = models.DateField(blank=True, null=True)
    fee_received_at = models.DateField(blank=True, null=True)
    fee_amount = models.IntegerField(
        choices=FEE_AMOUNT.CHOICES, default=FEE_AMOUNT.GENERAL
    )
    fee_payment_type = models.CharField(
        max_length=2,
        choices=FEE_PAYMENT_TYPE.CHOICES,
        default=FEE_PAYMENT_TYPE.BANK_TRANSFERENCE,
        blank=True,
    )
    fee_payment_reference = models.CharField(max_length=128, blank=True)
    remarks = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return f'{self.member.full_name} from {self.valid_from}'

    class Meta:
        ordering = ('valid_from', 'member')

    def save(self):
        if self.valid_until is None:
            self.valid_until = (
                self.valid_from + DEFAULT_MEMBERSHIP_PERIOD
                )
        super().save()


def add_new_member(
        first_name: str,
        last_name: str,
        email: str,
        username: str,
        address: str,
        rest_address: str,
        postal_code: str,
        city: str,
        phone: str,
        payment_date: Date,
        payment_reference: str,
        ) -> tuple[Member, str]:
    """Añadir un nuevo socio.

    Implica varios pasos, ya que hay que crear el usuario vinculado
    el socio, la entrada en la tabla Member y crear un primer pago
    de ese socio para el periodo correspondiente.

    Si todo va bien, devuelve el miembro (Instancia de Member) recien
    creado, y la contraseña asignada i nicialmente.

    Si se produce un error, no se realiza ningún cambio en la base de
    datos, ya que la operación se realiza en un transacción atómica.
    """
    password = generate_pronunciable_password()
    today = timezone.now().date()
    valid_from = payment_date
    delta = TimeDelta(days=366 if isleap(today.year) else 365)
    valid_until = max(payment_date, today) + delta
    with transaction.atomic():
        user = User.objects.create_user(
            username, email, password,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            date_joined=payment_date
            )
        member = Member(
            user=user,
            address=address,
            rest_address=rest_address,
            postal_code=postal_code,
            city=city,
            phone=phone,
            email=email,
            )
        member.save()
        _membership = Membership(
            member=member,
            valid_from=valid_from,
            valid_until=valid_until,
            fee_received_at=payment_date,
            fee_amount=FEE_AMOUNT.GENERAL,
            fee_payment_type=FEE_PAYMENT_TYPE.BANK_TRANSFERENCE,
            fee_payment_reference=payment_reference,
            ).save()
    return member, password
