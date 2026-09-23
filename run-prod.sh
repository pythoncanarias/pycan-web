#!/bin/bash

export ENV_ROOT=/home/jileon/apps/pycan-web/.venv
source ${ENV_ROOT}/bin/activate
python -m gunicorn wsgi:application --workers 2 -b 127.0.0.1:8001
