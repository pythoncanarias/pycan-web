import os
from django.conf import settings
import json


APPS = ("commons", "homepage", "events")


def glob(request):
    context = {"assets": {}}
    for app in APPS:
        manifest_path = os.path.join(
            settings.STATICFILES_DIRS[0], app, "rev-manifest.json")
        with open(manifest_path) as f:
            manifest_json = json.load(f)
        for k, v in manifest_json.items():
            key = os.path.join(app, k)
            value = os.path.join(settings.STATIC_URL, app, v)
            context["assets"][key] = value

    return context
