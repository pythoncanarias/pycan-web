#!/usr/bin/env python3

from email.message import EmailMessage
from itertools import chain
from pathlib import Path
from rq import Queue
import argparse
import logging
import logging.handlers
import os
import rq
import smtplib
import ssl
import sys

from prettyconf import config

from utils.results import Success, Failure, Result
from apps.commons.tasks import send_ntfy_message

def get_logger():
    log_handler = logging.handlers.RotatingFileHandler(
        filename='smoke_test.log',
        maxBytes=33554432, # 32 MB
        backupCount=8,
        )
    formatter = logging.Formatter(
        '%(asctime)s program_name [%(process)d]: %(message)s',
        '%b %d %H:%M:%S')
    log_handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)
    return logger


logger = get_logger()

def green(text: str) -> str:
    return f"\u001b[32m{text}\u001b[0m"

def red(text: str) -> str:
    return f"\u001b[31m{text}\u001b[0m"


OK = green("[OK ✓]")
ERROR = red("[ERROR ✖]")


def chk_env_file_exists_in_path() -> Result:
    """.env file exists somewhere in the path.
    """
    filename = '.env'
    base = Path.cwd()
    for base_name in chain([base], base.parents):
        full_path = base_name / filename
        if full_path.exists() and full_path.is_file():
            return Success(f'Found here: {full_path}')
    return Failure('File .env not found!')

def _get_redis_conn():
    import redis
    REDIS_SERVER = config('REDIS_SERVER', default='localhost')
    REDIS_PASSWORD = config('REDIS_PASSWORD', default='')
    REDIS_PROTOCOL = config('REDIS_PROTOCOL', default=2, cast=int)
    return redis.Redis(
        host=REDIS_SERVER,
        password=REDIS_PASSWORD,
        protocol=REDIS_PROTOCOL,
        )


def chk_redis_is_ready() -> Result:
    """Redis server is listening in the indicated host/port.
    """
    rds = _get_redis_conn()
    if rds.ping():
        return Success('Redis server is working')
    return Failure('Redis server is not working')


def chk_queues_are_working() -> Result:
    """Queues are defined and have workers assigned.
    """

    rds = _get_redis_conn()
    queue = Queue('default', connection=rds)
    job = queue.enqueue(send_ntfy_message, 'SmokeTest')
    return Success('Queued message by ntfy. Check in app.')


def chk_email_is_working():
    """Email subsystem is working.
    """
    EMAIL_SERVER = config('SMTP_SERVER')
    EMAIL_PORT = config('SMTP_PORT', cast=int, default=587)
    EMAIL_USERNAME = config('SMTP_USERNAME')
    EMAIL_PASSWORD = config('SMTP_PASSWORD')
    CONTACT_EMAIL = config('CONTACT_EMAIL')
    msg = EmailMessage()
    msg["to"] = 'euribates@gmail.com'
    msg["from"] = CONTACT_EMAIL
    msg["subject"] = "[Python Canarias Web] Smoke Test - Email"
    msg.set_content(
        "Prueba de envio de correo usando los parámetros"
        " de configuración de Python Canarias Web."
        )
    with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
        server.ehlo()  # Can be omitted
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        _result = server.send_message(msg)
        return Success('Email is working')
    return Failure('Email is NOT working')


def show_checks(checks):
    print('Availbale checks:', end="\n\n")
    width = max(len(check.__name__) for check in checks) + 1
    print('-' * width, '-' * (80 - width - 1))
    for check in checks:
        print(f'{check.__name__:<{width}} {green(check.__doc__.strip())}')


def run_checks(checks):
    num_checks = len(checks)
    passed = 0
    for functor in checks:
        name = functor.__name__
        print(f'▶ \033[1m{name}\033[0m:', end=' ', flush=True)
        if result := functor():
            passed += 1
            print(green(result.value), OK)
        else:
            print(red(result.error_message), ERROR)
    num_failed = num_checks - passed
    print()
    if num_failed:
        print(f"{ERROR} Some tests ({num_failed}/{num_checks}) did NOT pass.")
    else:
        print(f"{OK} All test ({num_checks}) pass.")
    sys.exit(num_failed)


if __name__ == '__main__':
    ALL_CHECKS = [
        chk_env_file_exists_in_path,
        chk_redis_is_ready,
        chk_email_is_working,
        chk_queues_are_working,
        ]
    parser = argparse.ArgumentParser(
        prog='SmokeTest',
        description='Verificación de entorno',
        )
    parser.add_argument(
        'check',
        nargs='*',
        choices=[_.__name__ for _ in ALL_CHECKS] + ['all'],
        )
    args = parser.parse_args()
    selected_checks = set(args.check)
    if not selected_checks:
        show_checks(ALL_CHECKS)
    elif selected_checks == {'all'}:
        run_checks(ALL_CHECKS)
    else:
        run_checks({
            _check for _check in ALL_CHECKS
            if _check.__name__ in selected_checks
            })
