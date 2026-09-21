Esta es una prueba de correo
enviada usando el adaptador emailer
a los siguientes correos.

{% for recipient in recipients %}- {{ recipient }}
{% endfor %}

## La plantilla está en markdown

Este correo debería tener dos versiones, una en texto
plano con el texto en _markdown_ y otra con el mismo
contenido pero en **html**.

## Datos incluidos por defecto

- La hora de creación del correo: {{ current_timestamp }}.
- La cabecera `to`: {{ to_email }}
- La lista de receptores: {{ recipients|pprint }}
- La cabecera `from`: {{ from_email }}
- La cabecera `subject`: {{ subject }}
- El nombre del fichero usado como plantilla: {{ template }}

## Datos acicionales

- Matraka: {matraka}



