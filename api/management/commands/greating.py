from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Greeting the user .'
    
    def handle(self,*args, **kwargs):
        self.stdout.write('Hello, ali  how are you.')