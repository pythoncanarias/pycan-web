import os
from django.conf import settings
import json


def glob(request):
    manifest_path = os.path.join(
        settings.STATICFILES_DIRS[0],
        "rev-manifest.json"
    )
    with open(manifest_path) as f:
        assets = json.load(f)
    return {"assets": assets}
