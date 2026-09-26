#!/usr/bin/env python3

from urllib.request import urlopen
import json

from django_rq import job


NTFY_URL = 'https://ntfy.sh/python_canarias'

@job
def send_ntfy_message(source:str=''):
    post_data = (
        f"{source}: Despliegue en producción de Python Canarias"
        ).encode()
    with urlopen(NTFY_URL, data=post_data) as response:
        data = response.read()
    response = json.loads(data)
    return response['id']
