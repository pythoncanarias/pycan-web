#!/usr/bin/env python3

from urllib.request import urlopen
from datetime import datetime as DateTime
import json

from django.utils import timezone

NTFY_URL = 'https://ntfy.sh/python_canarias'


def send_ntfy_message(source: str=''):
    now : DataTime = timezone.now()
    post_data = (
        f"{source}: Despliegue en producción de Python Canarias"
        f"\nEnviado el {now:%Y-%m-%d} a las {now:%H:%M:%S}"
        ).encode()
    with urlopen(NTFY_URL, data=post_data) as response:
        data = response.read()
    response = json.loads(data)
    return response['id']
