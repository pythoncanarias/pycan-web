#!/usr/bin/env bash

source ~/.virtualenvs/pycanweb/bin/activate

function loaddata () {
    echo -n "Loading $1";
    ./manage.py loaddata --verbosity 1 ./fixtures/$1.json;
    echo "[OK]";
}

# unzip -o backup.zip

loaddata "auth"
loaddata "about"
loaddata "api"
loaddata "admin"
loaddata "certificates"
loaddata "contenttypes"
loaddata "staticfiles"
loaddata "flatpages"
loaddata "commons"
loaddata "events"
loaddata "homepage"
loaddata "invoices"
loaddata "jobs"
loaddata "learn"
loaddata "legal"
loaddata "locations"
loaddata "members"
loaddata "messages"
loaddata "notices"
loaddata "organizations"
loaddata "quotes"
loaddata "schedule"
loaddata "sessions"
loaddata "sites"
loaddata "speakers"
loaddata "tickets"

