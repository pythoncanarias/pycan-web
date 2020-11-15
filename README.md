![Python Canarias Logo](https://github.com/pythoncanarias/docs/raw/master/logos/python-canarias/bitmaps/logo-python-canarias-color-372x128.png)

Website of [Python Canarias](pythoncanarias.es) 🚀 happily made with [Django](https://www.djangoproject.com/).

---

## Table of contents <!-- omit in TOC -->
- [Running with `docker-compose`](#running-with-docker-compose)
- [Python version and dependencies](#python-version-and-dependencies)
  * [Installing all dependencies in a virtual environment](#installing-all-dependencies-in-a-virtual-environment)
- [Node.js dependencies](#nodejs-dependencies)
- [Database](#database)
- [Customize your settings](#customize-your-settings)
- [Media](#media)
- [Launching services](#launching-services)
- [API](#api)
- [Adding a new section (app) to the project](#adding-a-new-section--app--to-the-project)


## Running with `docker-compose`

Ensure you have Docker and docker-compose installed.

Build the main app image and the Gulp (build tool) image:
```
docker-compose build
```

Run the database migrations:
```
docker-compose run pycan_web ./manage.py migrate
```

Add initial test data to the DB (You will need this to test the web app):
```
docker-compose run pycan_web ./manage.py dbload
```

Launch the app with the dependencies. This will start all services and keep your terminal blocked (You can Ctrl-C to stop all services):
```
docker-compose up
```

That's it, now visit http://localhost:8000/

Note that both the database and the web app bind their ports to the host. If you have port conflicts, you can export the environment variables `PYCAN_DB_PORT` and, `PYCAN_APP_PORT` to the desired ports in the host for, respectively, the database and the app, before running `docker-compose up`.

## Python version and dependencies

This project **requires Python 3.6**. From now on, `python3` is assumed to be Python 3.6.

The first level dependencies are listed in these files:

 * [`requirements.txt`](requirements.txt): packages for _production_
 * [`requirements-dev.txt`](requirements-dev.txt): additional requirements for _development_


### Installing all dependencies in a virtual environment

1. Install [`virtualenv`](https://virtualenv.pypa.io/en/latest/) and [`virtualenv-wrapper`](https://virtualenvwrapper.readthedocs.io/en/latest/).
2. Clone the repository: `git clone git@github.com:pythoncanarias/web.git`
3. Change to the project directory. Create the virtual environment and install all
   the dependencies for the project with the next lines:

```console
    $ mkvirtualenv -a . -p $(which python3) pycanweb
    $ pip install requirements.txt
    $ pip install requirements-dev.txt  # For developers
```

> This will install a virtual environment called `pycanweb` for the project, with Python 3, Django and all the rest Python dependencies.

## Node.js dependencies

Minimal versions of the required tools:

- `npm >= 5.6.0`
- `node >= 9.11.2`
- `gulp (cli) >= 2.0.1`
- `gulp (local version) >= 4.0.0`

There are some libraries (_css, js_) used on either the _frontend_ or the _development phase_. To install them, make:

```console
$ npm install
```

> ⚠️ This will create a bunch of folders and files under `node_modules`.

In order to use `gulp` correctly it is necessary to install:

```console
$ sudo npm install --global gulp-cli
```

## Database

We are using **PostgreSQL** as _database management system_. In order to configure the project correctly it is important to follow some indications:

1. Install [PostgreSQL](https://www.postgresql.org/download/).
2. Create a _database_ and a _user/password_ with full access to that database.
3. Set the following keys in the `.env` file: `DATABASE_NAME`, `DATABASE_USER` and `DATABASE_PASSWORD`.

Afterwards you can apply migrations with:

```console
$ workon pycanweb  # Activation of virtualenv
$ ./manage.py migrate
```

## Customize your settings

Feel free to change some of the settings creating a file called `.env` on the root of the project.

### Admin user <!-- omit in TOC -->

In order to create a user for the admin site of Django you should:

```console
$ workon pycanweb
$ ./manage.py createsuperuser
```

### Fixtures <!-- omit in TOC -->

Initially the database will be empty. Some fixtures will be needed to work with.

A bare minimum of data can be loaded by running:

```console
$ workon pycanweb
./manage.py dbload
```

## Media

It is important to properly set the key `MEDIA_ROOT` in the file `.env` for the server to locate the media assets.

## Launching services

In order to properly develop, you have to launch the following services:

- _Django_ development server:

```console
    $ workon pycanweb
    $ ./manage.py runserver
```

- _Gulp_ build system for static assets:

```console
    $ gulp watch
```

After that, you'll be able to access the project on: http://127.0.0.1:8000

> The changes made both in Python files or static files will be detected by the services and will reload them.

## API

You can check the documentation of the [public API](./docs/api.md).

## Adding a new section (app) to the project

Normally, when a new app (section) is needed in a Django project, it can be created as follows:

```console
$ ./manage.py startapp <app>
```

Based on the design of our project, some further steps must be taken in order to get the app well visualized:

1. Add `<app>` to the `APPS` constant on [gulp/config.js](gulp/config.js).
2. Create the file `<app>/static/<app>/css/main.scss` with, at least, the following content: `@import "commons/static/commons/css/base";`
3. Create the base template file at `<app>/templates/<app>/base.html` which extends from [commons/templates/base.html](commons/templates/base.html) as `base.html` and links to the stylesheet `<app>/custom.min.css` (_this file is generated by gulp_)
4. In order to create the corresponding item on header menu, add the app entry at [commons/templates/header.html](commons/templates/header.html).
