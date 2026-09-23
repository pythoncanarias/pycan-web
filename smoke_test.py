#!/usr/bin/env python3

import copy
import logging
import smtplib
import ssl
import sys
from datetime import UTC
from datetime import datetime as DateTime
from email.message import EmailMessage
from pathlib import Path

from prettyconf import config


def green(text: str) -> str:
    return f"\u001b[32m{text}\u001b[0m"

def red(text: str) -> str:
    return f"\u001b[31m{text}\u001b[0m"


OK = green("[OK ✓]")
ERROR = red("[ERROR ✖]")


def file_exists_in_path(filename, path):
    """Checks file exists somewhere in the path.

    If path is omited, it uses the current path.
    """
    ROOT = Path('/')
    path = Path(path)
    while True:
        full_path = path / filename
        if full_path.exists() and full_path.is_file():
            return True, f'Found here: {full_path}'
        if path == ROOT:
            break
        path = path.parent
    return False, 'Not found!'


def redis_is_ready():
    """Check a REDIS server is listening in the indicated host.

    Use `password` if suplied.
    """
    import redis
    REDIS_SERVER = config('REDIS_SERVER', default='localhost')
    REDIS_PASSWORD = config('REDIS_PASSWORD', default='')
    REDIS_PROTOCOL = config('REDIS_PROTOCOL', default=2, cast=int)
    try:
        rds = redis.Redis(
            host=REDIS_SERVER,
            password=REDIS_PASSWORD,
            protocol=REDIS_PROTOCOL,
            )
        timestamp = DateTime.now(tz=UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        rds.set('SmokeTest', timestamp)
        return True, 'Redis is working'
    except Exception as err:
        logging.exception(err)
        return False, 'Redis is NOT working'


def email_is_working():
    EMAIL_SERVER = config('AWS_SNS_SERVER')
    EMAIL_PORT = config('AWS_SNS_PORT', cast=int, default=587)
    EMAIL_USERNAME = config('AWS_SNS_USERNAME')
    EMAIL_PASSWORD = config('AWS_SNS_PASSWORD')
    CONTACT_EMAIL = config('CONTACT_EMAIL')
    msg = EmailMessage()
    msg["to"] = 'euribates@gmail.com'
    msg["from"] = CONTACT_EMAIL
    msg["subject"] = "[Python Canarias Web] Smoke Test - Email"
    msg.set_content(
        "Prueba de envio de correo usando los parámetros"
        " de configuración de Python Canarias Web."
        )
    try:
        with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
            server.ehlo()  # Can be omitted
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            result = server.send_message(msg)
            assert result == 1
        return True, 'Email is working'
    except Exception as err:
        logging.exception(err)
        return False, 'Email is NOT working'


class SmokeCheck:

    def __init__(self, name, functor, *args, **kwargs):
        self.name = name
        self.functor = functor
        self.args = copy.copy(args)
        self.kwargs = copy.copy(kwargs)

    def __str__(self):
        return self.name

    def __call__(self):
        try:
            status, message = self.functor(*self.args, **self.kwargs)
        except Exception as err:
            status = False
            message = str(err)
        return status, message


def main(all_checks):
    num_checks = len(all_checks)
    passed = 0
    for check in all_checks:
        print(f'▶ \033[1m{check.name}\033[0m:', end=' ', flush=True)
        try:
            status, message = check()
            if status:
                passed += 1
                print(message, OK)
            else:
                print(message, ERROR)
        except Exception as err:
            print(err, ERROR)
    num_failed = num_checks - passed
    if num_failed:
        print(f"{ERROR} Some tests ({num_failed}/{num_checks}) did NOT pass.")
    else:
        print(f"{OK} All test ({num_checks}) pass.")
    sys.exit(num_failed)


if __name__ == '__main__':
    ALL_CHECKS = [
        SmokeCheck('File .env exists', file_exists_in_path, ".env", Path.cwd()),
        SmokeCheck('Redis is operational', redis_is_ready),
        SmokeCheck('Email is working', email_is_working),
        ]
    main(ALL_CHECKS)
