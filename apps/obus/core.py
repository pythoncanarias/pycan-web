#!/usr/bin/env python3

from html import escape
from functools import partial

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
        from . import models
        models.Signal.new(level, item, message, self.username, **kwargs)

    archive = partial(publish, 'archive')
    debug = partial(publish, 'debug')
    delete = partial(publish, 'delete')
    error = partial(publish, 'error')
    info = partial(publish, 'info')
    insert = partial(publish, 'insert')
    panic = partial(publish, 'panic')
    test = partial(publish, 'test')
    update = partial(publish, 'update')
    warning = partial(publish, 'warning')

