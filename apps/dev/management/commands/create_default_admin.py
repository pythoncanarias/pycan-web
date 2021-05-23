from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Add a few entries to the database to allow a minimum developer experience
    """

    help = __doc__

    def handle(self, *args, **options):
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
