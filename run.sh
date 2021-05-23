#!/bin/bash

# Launch Django main entrypoint through UWSGI application server
# https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/uwsgi/

source ~/.virtualenvs/web/bin/activate
cd $(dirname $0)
exec uwsgi --ini uwsgi.ini
