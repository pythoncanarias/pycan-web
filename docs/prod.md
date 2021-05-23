# Production setup

Docker is not yet fully supported on production. Thus, a number of steps must be followed.

## Dependencies

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

## Settings

Some parameters must be set on `.env` file:

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
```

## Redis

We are using **Redis** for some services. In order to get it run properly it is important to follow some indications:

1. Install [Redis](https://redis.io/download).
2. Launch `run_rq.sh`

## Database

We are using **PostgreSQL** as _database management system_. In order to configure the project correctly it is important to follow some indications:

1. Install [PostgreSQL](https://www.postgresql.org/download/).
2. Create a _database_ and a _user/password_ with full access to that database.
