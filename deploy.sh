#!/bin/bash

# Commands to deploy project in production

git pull
pip install -r requirements.txt
npm install --no-save
gulp
python manage.py migrate
python manage.py collectstatic --noinput --clear
supervisorctl restart web
supervisorctl restart rq
