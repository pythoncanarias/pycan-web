import json
import uuid

import redis
from django.conf import settings

NAMESPACE = 'invitation'
MAX_CACHE_TIME = 7 * 24 * 60 * 60   # 7 days

redis_adapter = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def save_invitation(**kwargs):
    key = uuid.uuid4()
    full_key = f'{NAMESPACE}/{key}'
    redis_adapter.set(full_key, json.dumps(kwargs), MAX_CACHE_TIME)
    return key


def load_invitation(key):
    full_key = f'{NAMESPACE}/{key}'
    values = redis_adapter.get(full_key)
    return json.loads(values) if values else {}
