from django.db import models


class Ally(models.Model):
    '''Organizaciones/Asociaciones aliadas'''

    name = models.CharField('Nombre', max_length=120)
    description = models.CharField('Descripción', max_length=220)
    logo = models.ImageField(upload_to='about/allies/', blank=True)
    url = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
