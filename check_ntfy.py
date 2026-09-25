#!/usr/bin/env python3

from urllib.request import urlopen
import json

url = 'https://ntfy.sh/python_canarias'
post_data = "Hola mundo desde Python con urllib".encode('utf-8')
with urlopen(url, data=post_data) as response:
    data = response.read()
print(json.loads(data))
