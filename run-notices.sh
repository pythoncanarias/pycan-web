#!/bin/bash

# Dispatch notices from Python Canarias

source ~/.pyenv/versions/pycanweb/bin/activate
cd $(dirname $0)
exec python manage.py notices run
