#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps.events.models import Event


class EventConverter:
    regex = r'[A-Za-z0-9_\-]+'

    def to_python(self, value):
        event = Event.get_by_slug(value)
        if not event:
            raise ValueError("El identificador del evento es incorrecto")
        return event

    def to_url(self, value):
        if not isinstance(value, Event):
            raise ValueError(
                "Se necesita una instancia de la clase Event, pero"
                " es una instancia de {value.__class__.__name__}."
            )
        return value.slug
