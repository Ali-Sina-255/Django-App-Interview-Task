import csv
from django.core.management.base import BaseCommand
from dataentery.models import Student
# perposed command => python manage.py exportdata

class Command(BaseCommand):
    help ='Export data from Student model to CSV file'
    
    
    def handle(self, *args: csv.Any, **options: csv.Any) -> str | None:
        return super().handle(*args, **options)