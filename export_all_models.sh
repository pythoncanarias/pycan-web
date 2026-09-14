#!/bin/bash

# Speakers
./manage.py export_model speakers Social
./manage.py export_model speakers Speaker
./manage.py export_model speakers Contact

# Notice
./manage.py export_model notices NoticeKind
./manage.py export_model notices Notice

