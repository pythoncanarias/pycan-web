#!/usr/bin/env bash

set -e

python manage.py migrate
python manage.py collectstatic --noinput --clear
exec uwsgi --ini uwsgi.ini --socket /tmp/pycan/web.sock
