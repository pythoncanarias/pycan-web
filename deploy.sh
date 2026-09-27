#!/bin/bash

# Commands to deploy project in production

echo "$USER Empieza el despliegue"
source .venv/bin/activate

git pull
uv sync
python manage.py migrate
python manage.py collectstatic --noinput --clear
python smoke-test.py
python manage.py check --deploy

sudo systemctl restart nginx supervisor
