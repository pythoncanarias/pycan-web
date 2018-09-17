#!/bin/bash

cd "$(dirname "$0")"
pipenv run rq worker
