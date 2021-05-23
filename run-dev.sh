#!/bin/bash

# Launch Django development server on all IPs
# Valid for running inside Docker containers

python ./manage.py runserver 0.0.0.0:8000
