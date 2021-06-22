import json
import os

from django.conf import settings

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
    return dict(organization=Organization.load_main_organization())
