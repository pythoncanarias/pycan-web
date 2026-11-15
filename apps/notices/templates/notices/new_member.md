## {{ subject }} - {{ member }}
### {{ organization_name }}

Hola {{ member.full_name }} !

Gracias por haberte dado de alta como socio de Python Canarias. Tu ingreso
ha sido verificado y por tanto pasas a formar parte de nuestra asociación.

Eres el socio número {{ member.pk }}.

Puedes unirte a nuestro canal Telegram de socios y socias utilizando este
enlace de invitación:

    https://t.me/+P5fTFiaIXAOgxdT_

Igualmente podrás iniciar sesión en la página web de la asociación para
confirmar tus datos personales y gestionar los pagos de las cuotas:

	https://pythoncanarias.es/members/

Tus credenciales de acceso son el username que nos has pasado:

> `{{ member.user.username }}`

 y la contraseña:

> `{{ password }}`

Te recomendamos que modifiques la contraseña en tu primera conexión.

Si tienes cualquier duda, ponte en contacto con
nosotros en {{ contact_email }}. Gracias!

Un cordial saludo,<br>
la Junta Directiva.
