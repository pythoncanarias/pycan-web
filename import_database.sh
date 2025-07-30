#/bin/bash

scp jileon@www.pythoncanarias.es:web/exported.zip .
unzip exported.zip

source .env/bin/activate

./manage.py loaddata exported/about.json
./manage.py loaddata exported/organizations.json
./manage.py loaddata exported/quotes.json
./manage.py loaddata exported/locations.json
./manage.py loaddata exported/learn.json

./manage.py loaddata exported/events.json
./manage.py loaddata exported/schedule.json
./manage.py loaddata exported/speakers.json
./manage.py loaddata exported/tickets.json
./manage.py loaddata exported/invoices.json

./manage.py loaddata exported/jobs.json

./manage.py loaddata exported/members.json
./manage.py loaddata exported/notices.json

# ./manage.py loaddata exported/certificates.json

