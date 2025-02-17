#!/bin/bash

# Commands to deploy project in production

source ~/.pyenv/versions/pycanweb/bin/activate
git pull
pip install -r requirements.txt
npm install --no-save
gulp
python manage.py migrate
python manage.py collectstatic --noinput --clear
supervisorctl restart rq
supervisorctl restart web
