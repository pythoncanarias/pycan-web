#!/bin/bash

source ~/.virtualenvs/web/bin/activate
cd $(dirname $0)
exec python manage.py rqworker default low
