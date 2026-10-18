from django.db import models

from adapters.emailer import get_body
from apps.members.models import Member


class NoticeKindManager(models.Manager):

    def get_by_natural_key(self, code):
        return self.get(code=code)


class NoticeKind(models.Model):
    class Meta:
        verbose_name = 'Tipo de aviso'
        verbose_name_plural = 'Tipos de aviso'
        ordering = ['code']

    code = models.SlugField(
        max_length=32,
        help_text=(
            'Recuerde implementar la función con el mismo nombre'
            ' en apps/notices/repository.py'
            ),
        unique=True,
    )
    description = models.CharField(max_length=320)
    template = models.TextField(max_length=2048)
    days = models.IntegerField(
        default=0,
        help_text="Margen de días antes o después"
        " de la fecha de referencia",
    )
    enabled = models.BooleanField(default=True)

    objects = NoticeKindManager()

    @classmethod
    def load_notice_kind(cls, pk_or_code: str):
        try:
            if pk_or_code.isdigit():
                return cls.objects.get(pk=int(pk_or_code))
            else:
                return cls.objects.get(code=pk_or_code)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.description

    def natural_key(self):
        '''Se debe devolver una tupla con los valores de la clave
        natural, en el mismo orden es que las espera
        el método `get_by_natural_key` del Manager.
        '''
        return (self.code,)

    def enable(self):
        """Activa la regla.

        Es idempotente.
        """
        if not self.enabled:
            self.enabled = True
            self.save(update_fields='enabled', commit=True)
        
    def disable(self):
        """Desactiva la regla.

        Es idempotente.
        """
        if self.enabled:
            self.enabled = False
            self.save(update_fields='enabled', commit=True)

    def enqueue_notice(self, member, reference_date):
        message_text = get_body(
            [member.email],
            self.description,
            self.template,
            member=member,
            reference_date=reference_date,
            )
        notice = Notice(
            kind=self,
            member=member,
            reference_date=reference_date,
            message_text=message_text,
            )
        notice.save()
        return notice

    def notice_has_been_send(self, member, reference_date) -> bool:
        return (
            self.notice_set.filter(member=member)
            .filter(reference_date=reference_date)
            .exists()
            )


class Notice(models.Model):
    class Meta:
        verbose_name = 'Aviso para miembro'
        verbose_name_plural = 'Avisos para miembros'
        ordering = ['-send_at']

    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    kind = models.ForeignKey(NoticeKind, on_delete=models.PROTECT)
    reference_date = models.DateField()
    message_text = models.TextField(
        blank=True,
        default='',
        help_text=(
            'El texto del mensaje a enviar, procesado a partir de la'
            ' plantillla definida en su «NoticeKind».'
            ),
        )
    created_at = models.DateTimeField(auto_now_add=True)
    send_at = models.DateTimeField(blank=True, null=True, default=None)
    delivered_at = models.DateTimeField(blank=True, null=True, default=None)
    rejected_at = models.DateTimeField(blank=True, null=True, default=None)
    reply_code = models.PositiveIntegerField(default=0)
    reject_message = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default=None,
    )

    def __str__(self):
        return f"Notice {self.pk}"

    @classmethod
    def load_notice(cls, pk):
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            return None

    def status(self) -> str:
        if not self.send_at:
            return 'Waiting'
        elif self.send_at and not self.delivered_at and not self.rejected_at:
            return 'Sending'
        elif self.delivered_at:
            return 'Delivered'
        else:
            return f'Rejected: {self.reject_message}'

    def is_sent(self) -> bool:
        return self.send_at is not None

    def is_delivered(self) -> bool:
        return self.delivered_at is not None
