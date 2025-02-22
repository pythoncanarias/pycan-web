#/bin/bash

pg_dump --username pythoncanarias_user --dbname pythoncanarias_web --password > pythoncanarias.db

./manage.py dumpdata jobs --indent 4  > exported/jobs.json
