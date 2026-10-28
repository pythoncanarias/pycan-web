#!/bin/bash

# Commands to deploy project in production

echo "$USER Empieza el despliegue"
source .venv/bin/activate

git pull
uv sync
python manage.py migrate
python manage.py collectstatic --noinput --clear
python manage.py check --deploy
python smoke_test.py all

sudo systemctl restart nginx supervisor
