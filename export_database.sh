#!/usr/bin/env bash

source ~/.pyenv/versions/pycanweb/bin/activate

function dump () {
    echo -n "Dumping $1";
    ./manage.py dumpdata --verbosity 1 --indent 4 $1 > ./fixtures/$1.json
}


dumpdata('auth')
dumpdata('about')
dumpdata('api')
dumpdata('admin')
dumpdata('certificates')
dumpdata('contenttypes')
dumpdata('staticfiles')
dumpdata('flatpages')
dumpdata('commons')
dumpdata('events')
dumpdata('homepage')
dumpdata('invoices')
dumpdata('jobs')
dumpdata('learn')
dumpdata('legal')
dumpdata('locations')
dumpdata('members')
dumpdata('messages')
dumpdata('notices')
dumpdata('organizations')
dumpdata('quotes')
dumpdata('schedule')
dumpdata('sessions')
dumpdata('sites')
dumpdata('speakers')
dumpdata('tickets')

zip -r backup.zip fixtures/*.json
