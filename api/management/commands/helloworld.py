from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Prints Hello world.'
    def handle(self, *args, **kwargs):
        # we need to write the logic for the helo
        self.stdout.write("Hello, World")