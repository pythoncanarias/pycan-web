#!/bin/bash

# Launch Django development server on all IPs
# Valid for running inside Docker containers

if [[ ! -v VIRTUAL_ENV ]]; then
    echo "Activando entorno virtual"
    source .venv/bin/activate
fi
python ./manage.py runserver 0.0.0.0:8000
