#!/usr/bin/env bash

echo "${USER} starts pycanweb app";
source .venv/bin/activate
python -m gunicorn wsgi:application --workers 2 -b 127.0.0.1:$1
