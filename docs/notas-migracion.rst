Cambios aplicados a www.pythoncanarias.es
========================================================================

El **alojamiento ahora está en Hetzner**, en vez de en DigitalOcean. No
había mucho problema con DigitalOcean, pero Hetzner es Europeo, y un
pelín más barato.

El Sistema operativo es ahora **Ubuntu 24.04.5** LTS

El servicio de envío de correo, que era *sendgrid*, eliminó las cuotas
gratuitas, así que los envíos de correo dejaron de funcionar.

    Se ha cambiado a un sistema de **Amazon AWS, el SNS** (*Simple
    Notification Service*). Este es de pago, pero bastante razonable,
    cobran 0.16€ cada 1000 mensajes, así que quedaría muy por debajo de un
    euro al año. Miguel me comentó la alternativa de ``smtp2go``, que la
    cuenta gratuita nos daría 1000 mensajes gratis al mes. Podemos mirar
    ahora si lo pasamos ahí. Por ahora, tira, que es lo importante.

Actualizado **Python a 3.14.7**.

Actualizado **Django a a 6.1.1**.

Actualizado **PostgreSQL a la versión 16**.

Actualizado **Redis a 7.0.15**.

Actualizado **Bulma.css a 1.0.4**.

Actualizado **Awesome fonts a 7.3.1**.

Usamos **uv para gestión de paquetes**, entornos virtuales, etc.

**Ojo, Importante: Retirada toda la infraestructura de javascript en el
servidor** (``npm``, ``gulp``, etc.). Estaba muy obsoleta, con librerías
ya sin mantenimiento y con mogollón de agujeros de seguridad. Se puso
para intentar hacer una *One Single Page* para el evento, pero se ha
cambiado por una estructura tradicional y eso que nos ahorramos. Al no
tener a nadie experto en JS en *backend*, esto era un rémora para
futuros desarrollos.

En la web hay ahora la opción de elegir **modo oscuro o modo claro**.

**Hay rutas de migas de pan en todas las páginas** (*breadcrumbs*).

Opción de **página de socios**. Por ahora solo con la opción de cambiar
la dirección y el teléfono del socio. El siguiente paso es poder cambiar
la contraseña de usuario, que es algo que nos habían pedido varias
veces.

**Versión Beta**: Hay ahora mismo dos direcciones, en
``wwww.pythoncanarias.es`` está desplegada la rama ``main`` del
repositorio, en ``beta.pythoncanarias.es`` está desplegada la rama
``dev``. Ahora mismo ambas son la misma, pero la idea es poder realizar
cambios en la rama ``dev`` y poder verlos antes de pasarlos a ``main``.
No sé porqué lo llame ``beta``. Es lo que la gente suele llamar
preproducción o preexplotación.

Y alguna cosilla más que se me habrá pasado, conociéndome.

