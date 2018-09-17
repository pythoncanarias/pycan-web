#!/bin/bash

cd "$(dirname "$0")"
export DJANGO_SETTINGS_MODULE=main.settings
pipenv run rq worker
