#!/usr/bin/env python3

from html import escape
from functools import partialmethod

from django.db.models import Model
from django.contrib import messages

from apps.commons.filters import as_markdown



class BusBase:

    def __init__(self, request, messages_system=messages):
        assert request.user.is_authenticated
        self.request = request
        self.username = request.user.username
        self.messages = messages_system

    def message_user(self, level: str, msg: str):
        text = as_markdown(escape(msg))
        if text[:3] == '<p>':
            text = text[3:]
        if text[-4:] == '</p>':
            text = text[-4:]
        match level:
            case 'debug':
                self.messages.debug(self.request, text)
            case 'warning' | 'archive' | 'delete':
                self.messages.warning(self.request, text)
            case 'error' | 'panic':
                self.messages.error(self.request, text)
            case 'info' | 'test':
                self.messages.info(self.request, text)
            case 'success' | 'insert' | 'update':
                self.messages.success(self.request, text)
            case _:
                self.messages.error(self.request, text)

    def publish(self, level: str, item: Model, message: str, **kwargs):
        from .models import Signal, SignalLevel
        if not isinstance(item, Model) and not hasattr(item, 'pk'):
            raise ValueError(
                "Solo se pueden publicar en el bus"
                " instancias de clases derivadas de la clase Model"
                " de Django,"
                " o de clases que permitan el acceso a su clave primaria"
                " con el atributo ``pk``\n\n."
                " El sujeto indicado: {escape(repr(item))}"
                f" es de tipo {escape(repr(type(item)))}"
                )
        user_feedback = kwargs.pop('user_feedback', True)
        if user_feedback:
            self.message_user(level, message)
        Signal.new_signal(
            item,
            message,
            SignalLevel.load_signal_level(level),
            self.username,
            **kwargs,
            )

    archive = partialmethod(publish, 'archive')
    debug = partialmethod(publish, 'debug')
    delete = partialmethod(publish, 'delete')
    error = partialmethod(publish, 'error')
    info = partialmethod(publish, 'info')
    insert = partialmethod(publish, 'insert')
    panic = partialmethod(publish, 'panic')
    test = partialmethod(publish, 'test')
    update = partialmethod(publish, 'update')
    warning = partialmethod(publish, 'warning')

