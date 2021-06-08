#!/bin/bash

# Dispatch notices from Python Canarias

source ~/.virtualenvs/web/bin/activate
cd $(dirname $0)
exec python manage.py notices run
