#!/bin/bash

# Launch worker for Redis Queue
# https://python-rq.org/

source ~/.pyenv/versions/pycanweb/bin/activate
cd $(dirname $0)
exec python manage.py rqworker default low
