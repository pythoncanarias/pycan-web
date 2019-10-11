# Web

Web for Python Canarias made in Django.

## Python dependencies

### Pipenv

This projects uses [Pipenv](https://pipenv.readthedocs.io/en/latest/).

> Pipenv is a tool that aims to bring the best of all packaging worlds (bundler, composer, npm, cargo, yarn, etc.) to the Python world.

Some of its great features are:

- Enables truly deterministic builds, while easily specifying only what you want.
- Generates and checks file hashes for locked dependencies.
- Automatically install required Pythons, if pyenv is available.
- Automatically finds your project home, recursively, by looking for a Pipfile.
- Automatically generates a Pipfile, if one doesn’t exist.
- Automatically creates a virtualenv in a standard location.
- Automatically adds/removes packages to a Pipfile when they are un/installed.
- Automatically loads .env files, if they exist.

### If you prefer to use virtualenv and friends

You can get a requirements file as a subproduct of the Pipfile (This is why we
removed the `requirements.txt` and the `requirements-dev.txt` from the repo).

This command allows you to generate a proper `requirements.txt` from the Pipfile:

    pipenv lock --requirements > requirements.txt

Use this command if you want a requirements file for developers:

    pipenv lock --requirements --dev > requirements-dev.txt


#### Proceed

After you have cloned the repo, make:

~~~console
$ pipenv install --python 3.6
~~~

This will install a virtual environment for the project, with Python 3.6, Django and all the rest Python dependencies.

## Node.js dependencies

Minimal versions:

- `npm >= 5.6.0`
- `node >= 9.11.2`
- `gulp (cli) >= 2.0.1`
- `gulp (local version) >= 4.0.0`

There are some libraries (*css, js*) used on either the *frontend* or the *development phase*. To install them, make:

~~~console
$ npm install
~~~

> This will create a bunch of folders and files under `node_modules`.

In order to use `gulp` correctly it is necessary to install:

~~~console
$ sudo npm install --global gulp-cli
~~~

## Developing

### EditorConfig

Please install the corresponding extension of [EditorConfig](https://editorconfig.org/) in your favourite editor. Thus your editor will pick the settings stored in `.editorconfig`.

This configuration avoids conflicts with a lot of settings, mainly with tabs widths.

### Customize your settings

Feel free to change some of the settings creating a file called `.venv` on the root of the project.

### Database

We are using **PostgreSQL** as *database management system*. In order to configure the project correctly it is important to follow some indications:

1. Install [PostgreSQL](https://www.postgresql.org/download/).
2. Create a *database* and a *user/password* with full access to that database.
3. Set the following keys in the `.env` file: `DATABASE_NAME`, `DATABASE_USER` and `DATABASE_PASSWORD`.

Afterwards you can apply migrations with:

~~~console
$ pipenv run python manage.py migrate
~~~

#### Admin user

In order to create a user for the admin site of Django you should:

~~~console
$ pipenv run python manage.py createsuperuser
~~~

#### Fixtures

Initially (and obviously) the database will be empty. Some `fixtures` will be needed to work with.

### Media

It is important to set property the key `MEDIA_ROOT` in the file `.env`

### Launching services

In order to develop, you have to launch the following services:

~~~console
$ pipenv run python manage.py runserver # on one terminal
$ gulp watch                 # on another terminal
~~~

After that, you'll be able to access the project on http://127.0.0.1:8000

The changes made both in Python files or static files will be detected by the services and will reload them.

### Model graphs

~~~console
$ pipenv run python manage.py graph_models events organizations locations speakers tickets schedule -g -S -o models.png
~~~

### API

There are new documentation about the [public API](./docs/api.md).
