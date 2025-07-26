#/bin/bash

pg_dump --username pythoncanarias_user --dbname pythoncanarias_web --password > pythoncanarias.db

./manage.py dumpdata about --indent 4  > exported/about.json
./manage.py dumpdata certificates --indent 4  > exported/certificates.json
./manage.py dumpdata certificates --indent 4  > exported/certificates.json
./manage.py dumpdata events --indent 4  > exported/events.json
./manage.py dumpdata invoices --indent 4  > exported/invoices.json
./manage.py dumpdata jobs --indent 4  > exported/jobs.json
./manage.py dumpdata learn --indent 4  > exported/learn.json
./manage.py dumpdata locations --indent 4  > exported/locations.json
./manage.py dumpdata members --indent 4  > exported/members.json
./manage.py dumpdata notices --indent 4  > exported/notices.json
./manage.py dumpdata organizations --indent 4  > exported/organizations.json
./manage.py dumpdata quotes --indent 4  > exported/quotes.json
./manage.py dumpdata schedule --indent 4  > exported/schedule.json
./manage.py dumpdata speakers --indent 4  > exported/speakers.json
./manage.py dumpdata tickets --indent 4  > exported/tickets.json

zip -r exported.zip exported

