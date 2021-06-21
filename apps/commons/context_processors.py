import json
import os

from django.conf import settings
from django.core.cache import cache

from apps.organizations.models import Organization


def glob(request):
    static_folder_path = settings.STATIC_ROOT
    if settings.DEBUG:
        static_folder_path = settings.STATICFILES_DIRS[0]

    manifest_path = os.path.join(static_folder_path, "rev-manifest.json")
    with open(manifest_path) as f:
        try:
            assets = json.load(f)
        except Exception:
            assets = False
    return {"assets": assets}


def main_organization_data(request):
    key = "web.organization"
    org = cache.get(key)
    if org is None:
        print("Cache MISS")
        org = Organization.load_main_organization()
        cache.set(key, org, timeout=604800)  # 7 días
    else:
        print("Cache hit")
    return {
        'organization': org,
    }
