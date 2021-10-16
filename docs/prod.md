# Configuración de Producción

Docker no está soportado aún en producción. Deben seguirse estos pasos:

## Dependencias

### Python

- `Python 3.6`

```console
$ pip install requirements.txt
```

### Node.js

- `npm >= 5.6.0`
- `node >= 9.11.2`
- `gulp (cli) >= 2.0.1`
- `gulp (local version) >= 4.0.0`

```console
$ npm install
```

## Ajustes

Estos parámetros deben establecerse en un fichero `.env`:

```console
DEBUG = False
SECRET_KEY = <something unique>
STRIPE_PUBLIC_KEY = <stripe public api key>
STRIPE_SECRET_KEY = <stripe secret api key>
ALLOWED_HOSTS = pythoncanarias.es
TIME_ZONE = <timezone where the server is located>
STATIC_ROOT = <path to the static assets folder>
MEDIA_ROOT = <path to the media files folder>
DATABASE_NAME = <name of the database>
DATABASE_USER = <user for the database>
DATABASE_PASSWORD = <password for the database>
SENDGRID_API_KEY = <sendgrid api key>
TWITTER_API_KEY = <twitter api key>
TWITTER_API_SECRET_KEY = <twitter api secret key>
TWITTER_ACCESS_TOKEN = <twitter access token>
TWITTER_ACCESS_TOKEN_SECRET = <twitter access token secret>
```

## Redis

Usamos **Redis** para algunos servicios. Sigue estas indicaciones para confirgurarlo:

1. Instala [Redis](https://redis.io/download).
2. Ejecuta `run-rq.sh`

## Notificaciones

Tenemos una app de Django para enviar notificaciones por email. Para enviar estas notificaciones, es necesario ejecutar el script `run-notices.sh` periódicamente (por ejemplo diariamente) a través de cron.

## Base de datos

Usamos **PostgreSQL** como base de datos.

1. Instala [PostgreSQL](https://www.postgresql.org/download/).
2. Crea una base de datos y unas credenciales con acceso completo a la misma.
