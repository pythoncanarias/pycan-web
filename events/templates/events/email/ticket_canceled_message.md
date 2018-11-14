## Entrada cancelada 

La entrada para el evento {{ event.name }}  ha sido cancelada.

Los datos de la entrada son los siguientes:

- Evento: <a href="{{ event.get_full_url}}">{{ event.name }}</a>
- Número de ticket: {{ ticket.number }}
- Tipo de entrada: {{ category.name }}
- Titular de la entrada: {{ ticket.customer_name }} {{ ticket.customer_surname }}

Si cree que hay algún error en esta cancelación, por favor póngase
en contacto con nosotros en `info@pythoncanarias.es`.
