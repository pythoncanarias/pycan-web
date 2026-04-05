#!/usr/bin/env bash

./manage.py dumpdata --indent 4 auth > fixtures/auth.json
./manage.py dumpdata --indent 4 about > fixtures/about.json
./manage.py dumpdata --indent 4 api > fixtures/api.json
./manage.py dumpdata --indent 4 admin > fixtures/admin.json
./manage.py dumpdata --indent 4 certificates > fixtures/certificates.json
./manage.py dumpdata --indent 4 contenttypes > fixtures/contenttypes.json
./manage.py dumpdata --indent 4 staticfiles > fixtures/staticfiles.json
./manage.py dumpdata --indent 4 flatpages > fixtures/flatpages.json
./manage.py dumpdata --indent 4 commons > fixtures/commons.json
./manage.py dumpdata --indent 4 events > fixtures/events.json
./manage.py dumpdata --indent 4 homepage > fixtures/homepage.json
./manage.py dumpdata --indent 4 invoices > fixtures/invoices.json
./manage.py dumpdata --indent 4 jobs > fixtures/jobs.json
./manage.py dumpdata --indent 4 learn > fixtures/learn.json
./manage.py dumpdata --indent 4 legal > fixtures/legal.json
./manage.py dumpdata --indent 4 locations > fixtures/locations.json
./manage.py dumpdata --indent 4 members > fixtures/members.json
./manage.py dumpdata --indent 4 messages > fixtures/messages.json
./manage.py dumpdata --indent 4 notices > fixtures/notices.json
./manage.py dumpdata --indent 4 organizations > fixtures/organizations.json
./manage.py dumpdata --indent 4 quotes > fixtures/quotes.json
./manage.py dumpdata --indent 4 schedule > fixtures/schedule.json
./manage.py dumpdata --indent 4 sessions > fixtures/sessions.json
./manage.py dumpdata --indent 4 sites > fixtures/sites.json
./manage.py dumpdata --indent 4 speakers > fixtures/speakers.json
./manage.py dumpdata --indent 4 tickets > fixtures/tickets.json
zip backup.zip fixtures/*.json
