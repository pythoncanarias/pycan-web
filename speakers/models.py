from urllib.parse import urljoin

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models


class Social(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=32, unique=True)
    base_url = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'social network'
        verbose_name_plural = 'social networks'


class Speaker(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    bio = models.TextField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    photo = models.ImageField(
        upload_to='speakers/speaker/',
        blank=True,
    )

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)

    def socials_for_display(self):
        return [{'code': c.social.code, 'href': c.href}
                for c in self.contacts.order_by('social__name')]

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return static('speakers/img/noavatar.png')


class Contact(models.Model):
    social = models.ForeignKey(
        Social,
        on_delete=models.PROTECT,
        related_name='contacts'
    )
    speaker = models.ForeignKey(
        Speaker,
        on_delete=models.PROTECT,
        related_name='contacts'
    )
    identifier = models.CharField(max_length=128)

    def __str__(self):
        return self.href

    @property
    def href(self):
        return urljoin(self.social.base_url, self.identifier)
