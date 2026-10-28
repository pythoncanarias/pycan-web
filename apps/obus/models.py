#!/usr/bin/env python3

import uuid
import json

from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

MAX_LENGTH_FOR_PRIMARY_KEY = 32
MAX_LENGTH_FOR_CLASS_NAME = 48
MAX_LENGTH_FOR_DESCRIPTION = 2048
MAX_LENGTH_FOR_USERNAME = 62


class SignalLevel(models.Model):
    """Niveles del suceso.

    Estos son los niveles predefinidos:

    | nivel       | descripción                      |
    |:-----------:|:---------------------------------|
    | ``archive`` | Borrado lógico o archivado       |
    | ``debug``   | Mensajes de depuración           |
    | ``delete``  | Borrado de datos existentes      |
    | ``error``   | Mensajes de error                |
    | ``info``    | Mensajes informativos            |
    | ``insert``  | Alta de nuevos datos             |
    | ``panic``   | Mensaje de error crítico         |
    | ``test``    | Mensajes de prueba               |
    | ``update``  | Modificación de datos            |
    | ``warning`` | Mensajes de aviso                |

    Los niveles ``insert``, ``update``, ``archive`` y ``delete`` se
    consideran subtipos concretos del tipo ``info``.
    """

    class Meta:
        """Metadatos de la clase SignalLevel.
        """
        db_table = 'obus_signal_level'
        verbose_name = 'Nivel del suceso'
        verbose_name_plural = 'Niveles de los sucesos'

    id_level = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=28, unique=True)

    def __str__(self) -> str:
        return self.name

    def to_json(self) -> str:
        """Devuelve una representación textual en formato json.
        """
        return json.dumps({
            'id_level': self.id_level,
            'name': self.name,
            }, indent=4)


class Signal(models.Model):
    """Resumen de un suceso (cambio de estado) que afecta a un objeto.

    Campos:

    - ``id_signal`` (``UUID``): Clave primaria del evento. Por defecto usa
      ``uuid.uuid1``.

    - ``level`` (``str``): Nivel del evento. Es una clave foránea a
      ``CaseLevel``, donde se registran los diferentes tipos de
      niveles de evento disponibles.

    - ``subject`` (``str``): La clave primaria, en JSON, del objeto cuyo
      estado ha sido modificado. El valor pasado se pasa por
      ``json.dumps``.

      Es una clave foránea, pero no se implementa como tal para
      simplificar el sistema y que se pueda adaptar a cualquier modelo.

      Esto complica el acceso a los eventos desde el punto de vista del
      objeto, pero simplifica por otro lado al no tener que mantener una
      clave foránea y se puede adaptar por tanto a casi cualquier
      sistema (siempre que la representación de la clave foránea quepa
      en 32 caracteres).

    - ``class_name`` (``str``): El nombre de la clase del sujeto. En
      principio con esta información y la representación de la clave
      primaria debería bastar para poder identificar al sujeto en la
      base de datos.

    - ``message`` (``str``): Descripción textual del cambio sufrido por
      el modelo.

    - ``published_at`` (``DateTime``): Fecha y hora del momento en
      que se ha notificado el evento. Si no se especifica --que es lo
      normal--, se usará la fecha y hora en que se almacena en la
      base de datos.

    - ``username`` (``str``): Identificación del usuario que ha
      provocado el cambio. Idealmente, el ``login`` o ``username`` del
      usuario. Al igual que con el campo ``subject``, debería ser un
      ``ForeignKey`̀a la clase ``User`` o similar, pero se deja abierto
      para hacer el sistema más flexible y capaz de funcionar con otros
      sistemas de autenticación, aparte del de Django.

    - payload (str): Una representación en JSON de otros datos que
      puedan enriquecer la información sobre el evento.

    """

    class Meta:
        """Metadatos de la case Case.

        """
        db_table = 'obus_signal'
        verbose_name = 'suceso'
        verbose_name_plural = 'sucesos'
        ordering = ['published_at']

    id_signal = models.UUIDField(
        primary_key=True,
        default=uuid.uuid1,
        editable=False,
        )
    level = models.ForeignKey(SignalLevel,
        on_delete=models.PROTECT,
        related_name='signals'
        )
    subject = models.CharField(max_length=MAX_LENGTH_FOR_PRIMARY_KEY)
    class_name = models.CharField(max_length=MAX_LENGTH_FOR_CLASS_NAME)
    message = models.CharField(max_length=MAX_LENGTH_FOR_DESCRIPTION)
    published_at = models.DateTimeField(auto_now_add=True, editable=False)
    username = models.CharField(max_length=MAX_LENGTH_FOR_USERNAME)
    payload = models.JSONField(
        encoder=DjangoJSONEncoder,
        blank=True,
        default=None,
        null=True,
        )

    def __str__(self):
        return f'{self.class_name}[{self.subject}]: {self.level} {self.message}'

    @classmethod
    def new_case(cls, item, message, level, username, **kwargs):
        _primary_key = json.dumps(item.pk)[:MAX_LENGTH_FOR_PRIMARY_KEY]
        _class_name = item.__class__.__name__[:MAX_LENGTH_FOR_CLASS_NAME]
        _message = message[:MAX_LENGTH_FOR_DESCRIPTION]
        _username = str(username)[:MAX_LENGTH_FOR_USERNAME]
        signal = cls(
            level=level,
            subject=_primary_key,
            class_name=_class_name,
            message=message,
            username=_username,
            payload=kwargs.copy(),
            )
        signal.save()
        return signal


