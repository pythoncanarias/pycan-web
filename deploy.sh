#!/bin/bash

# Commands to deploy project in production

echo "$USER Empieza el despliegue"
source .venv/bin/activate
git pull
uv sync
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput --clear
# supervisorctl restart pycan-rq
supervisorctl restart pycan-web
