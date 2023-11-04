"""
Django command to wait for the database to be available
"""
import time
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for the database."""

    def handle(self, *args, **options):
        self.stdout.write("waiting for the database to wake...")
        dp_wake = False
        while not dp_wake:
            try:
                self.check(databases=['default'])
                dp_wake = True
            except (OperationalError, Psycopg2Error):
                self.stdout.write('database appears to be sleeping, \
                                   wait for 1 second')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('database is awake now!'))
