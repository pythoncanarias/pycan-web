#!/usr/bin/env python3

from urllib.request import urlopen
import json

url = 'https://ntfy.sh/python_canarias'
post_data = b"Hola mundo desde Python con urllib"
with urlopen(url, data=post_data) as response:
    data = response.read()
print(json.loads(data))
