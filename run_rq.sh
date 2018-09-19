#!/bin/bash

cd "$(dirname "$0")"
pipenv run python manage.py rqworker default low
