#!/usr/bin/env bash

if [[ ! -v VIRTUAL_ENV ]]; then
    echo "Activando entorno virtual"
    source .venv/bin/activate
else
    echo "Ya activado entorno virtual: ${VIRTUAL_ENV}"
fi
python manage.py rqworker --with-scheduler high default low
