from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Add a few entries to the database to allow a minimum developer experience
    """

    help = __doc__

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(username='admin')
        admin.is_superuser = True
        admin.is_staff = True
        admin.set_password('admin')
        admin.save()
