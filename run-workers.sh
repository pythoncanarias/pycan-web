#!/usr/bin/env bash

cd /home/jileon/apps/pycan-web
source .venv/bin/activate
uv run python manage.py rqworker --with-scheduler high default low
