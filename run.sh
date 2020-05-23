#!/bin/bash
# Master script.

source ~/.virtualenvs/web/bin/activate
cd $(dirname $0)
exec uwsgi --ini uwsgi.ini
