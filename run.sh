#!/bin/bash
# Master script.

cd "$(dirname "$0")"
PYTHON_VENV=$(pipenv --venv)
exec uwsgi --home $PYTHON_VENV --ini uwsgi.ini
