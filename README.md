# Web

Web for Python Canarias

## Python dependencies

This projects uses `pipenv`. After you have cloned the repo, make:

~~~console
$ pipenv install --python 3.6
~~~

This will install a virtual environment for the project, with Python 3.6, Django and all the rest Python dependencies.

## Node.js dependencies

There are some libraries (*css, js*) used on either the *frontend* or the *development phase*. To install them, make:

~~~console
$ npm install
~~~

## Developing

### EditorConfig

Please install the corresponding extension of [EditorConfig](https://editorconfig.org/) in your favourite editor. Thus your editor will pick the settings stored in `.editorconfig`.

This configuration avoids conflicts with a lot of settings, mainly with tabs widths.

### Customize your settings

Feel free to change some of the settings creating a file called `.venv` on the root of the project.

### Launching services

In order to develop, you have to launch the following services:

~~~console
$ pipenv shell
$ python manage.py runserver # on one terminal
$ gulp watch                 # on another terminal
~~~

After that, you'll be able to access the project on http://127.0.0.1:8000

The changes made both in Python files or static files will be detected by the services and will reload them.
