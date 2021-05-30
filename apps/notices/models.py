from django.db import models
from django.conf import settings

from apps.members.models import Member


def get_list_of_internal_apps():
    internal_apps = []
    for app_name in settings.INSTALLED_APPS:
        if app_name.startswith('apps.'):
            internal_apps.append(app_name[5:])
    return zip(internal_apps, internal_apps)



class NoticeKind(models.Model):

    class Meta:
        unique_together = ('app', 'code',)
        verbose_name = 'Tipo de aviso'
        verbose_name_plural = 'Tipos de aviso'

    app = models.SlugField(max_length=24, choices=get_list_of_internal_apps())
    code = models.SlugField(max_length=32)
    description = models.CharField(max_length=320)
    template = models.CharField(max_length=512)

    def __str__(self):
        return f"{self.app}.{self.code}: {self.description}"


class Notice(models.Model):

    class Meta:
        verbose_name = 'Aviso para miembro'
        verbose_name_plural = 'Avisos para miembros'

    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    kind = models.ForeignKey(NoticeKind, on_delete=models.PROTECT)
    reference_date = models.DateField()
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


    def is_sent(self):
        return self.send_at is not None

    def is_delivered(self):
        return self.delivered_at is not None
