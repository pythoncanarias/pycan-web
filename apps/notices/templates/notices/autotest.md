## {{ subject }}
### {{ organization_name }}

Hola **{{ member.full_name }}**, este correo es una prueba de los
envíos de notificaciones a los socios de **{{ organization_name }}**.

Estos son los datos que tenemos de ti:

- Eres el socio nº: {{ member.member_id }}
- Tu identificador de usuario (_login_) es: `{{ member.user.username }}`
- Nombre: {{ member.user.first_name }}
- Apellidos: {{ member.user.last_name }}
- Dirección: {{ member.address }}
    {{ member.postal_code }} {{ member.city }}
- Teléfono: {{ member.phone }}
- Correo electrónico: {{ member.email }}
- Próxima fecha de renovación: {{ member.get_valid_until }}
{% if member.is_founder %}- Eres  **miembro fundador**.{% endif %}
{% if member.is_honorary %}- Eres  **miembro honorario**.{% endif %}

Puedes consultar y modificar estos datos en:

[{{ login_url }}]({{ login_url }})

Un cordial saludo,<br>
La Junta Directiva.
