#!/usr/bin/env python3

"""
Módulo ``results``
------------------------------------------------------------------------

Una implementación muy sencilla de las monadas_ de resultado.  Se
definen dos clases, ::py:class:`Success` y :py:class:`Failure`.  La
primera se usa para informar de un resultado correcto, mientras que la
segunda es para informar de un fallo o error. Los objetos de tipo
``Success`` tienen un atributo ``value`` que les permite acceder al
valor retornada. Los objetos de tipo ``Failure`` tiene una propiedad
``error_message`` con información acerca del error que ha sucedido.

Cualquier intento de acceder a la propiedad ``value`` de un objeto de
tipo ``Failure`` elevará una excepción de tipo ``ValueError``. De igual
manera, todo intento de acceder al atributo ``error_message`` de un
objeto de tipo ``Success`` elevará la misma excepción.

Tanto los objetos de tipo ``Success`` como los de tipo ``Failure``
tienen los métodos ``is_success()`` e ``is_failure()``, que devuelven
los valores booleanos correspondientes.

Es decir, para todos los objetos de la clase ``Success``, se cumple que
:code:`is_success() is True`` y :code:``is_failure() is False``.

Igualmente, para todos los objetos de la clase ``Failure``, se cumple
que :code:`is_success() is False`` y :code:``is_failure() is True``.

.. _monadas:: https://es.wikipedia.org/wiki/M%C3%B3nada_(programaci%C3%B3n_funcional)
"""

from typing import Union

__all__ = ['Success', 'Failure', 'Result']


class Success:
    """Representación de un resultado válido.

    El valor del resultado está en el atributo ``value``. Si no se
    indica, ``value`` vale por defecto ``True``. Si se evalua
    como booleano, no importa el valor que contenga el atribito,
    siempre evaluará a ``True``.

    Params:

        value (Any): Un valor para incluir en el resultado (opcional)
    """

    def __init__(self, value=True):
        """constructor de la clase success.

        Params:

            value (any): el valor a incluir en el resultado.
        """
        self.value = value

    def __bool__(self) -> bool:
        """Resultado se intenta evaluar una instancia como booleno.

        Para los objetos de tipo ``Success`` es siempre ``True``.
        """
        return True

    def is_success(self) -> bool:
        """Permite detreminar si esta instancia en de tipo ``Success``.

        Returns:

            Las instancias de tipo ``Success`` siempre devuelven
            ``True``.

        """
        return True

    def is_failure(self) -> bool:
        """Permite detreminar si esta instancia en de tipo ``Failure``.

        Returns:

            Las instancias de tipo ``Success`` siempre devuelven
            ``False``.

        """
        return False

    def __repr__(self):
        """Representación de una instancia tipo ``Success``.
        """
        return f'Success({self.value!r})'

    @property
    def error_message(self):
        """Atributo prohibido para las instancias de ``Success``.

        Cualquier intento de acceder a ``error_message`` en una
        instancia de Sucesss elevará una excepción de tipo
        ``ValueError``.
        """
        raise ValueError(
            'No se puede acceder a la propiedad error_message'
            ' en una instancia de Success.'
            )


class Failure:
    """Representación de un resultado inválido o erroneo.

    En el atributo ``error_message`` se puede acceder a una descripción
    del error. Si se evalua como booleano, siempre evaluará a ``False``.

    Atributos:

        error_message (str): Un mensaje explicativo de por qué
           el resultado es erroneo

        code (str): Un código de identificación del error (opcional)

    """

    def __init__(self, error_message, extra=None):
        """Constructor de la clase Failure.

        Parameters:

            error_message (str): Mensaje de explicación.

            code (str): Código de error (Opcinal)
        """
        self.error_message = error_message
        self.extra = extra

    def __bool__(self):
        """Resultado de intenta evaluar una instancia como booleno.

        Para los objetos de tipo ``Failure`` es siempre ``False``.
        """
        return False

    def is_success(self) -> bool:
        """Permite detreminar si esta instancia en de tipo ``Failure``.

        Returns:

            Las instancias de tipo ``Failure`` siempre devuelven
            ``False``.
        """
        return False

    def is_failure(self) -> bool:
        """Permite detreminar si esta instancia en de tipo ``Failure``.

        Returns:

            Las instancias de tipo ``Failure`` siempre devuelven
            ``True``.

        """
        return True

    def __repr__(self) -> str:
        """Representación de una instancia tipo ``Failure``.
        """
        if self.extra is None:
            return f'Failure({self.error_message!r})'
        return f'Failure({self.error_message!r}, extra={self.extra!r})'

    def __str__(self) -> str:
        """Versión texto de una instancia tipo ``Failure``.
        """
        return f'Error: {self.error_message}'

    @property
    def value(self):
        """Atributo prohibido para las instancias de ``Failure``.

        Cualquier intento de acceder a ``value`` en una
        instancia de ``Failure`` elevará una excepción de tipo
        ``ValueError``.

        """
        raise ValueError(
            'No se puede acceder a la propiedad value'
            ' en una instancia de Failure.'
            )


Result = Union[Success, Failure]
