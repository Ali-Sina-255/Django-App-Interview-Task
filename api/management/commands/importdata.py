from django.core.management.base import BaseCommand, CommandError
from api.models import Job
import csv
from django.apps import apps




file_path = '/home/ali/Documents/job_data.csv'

class Command(BaseCommand):
    help = 'Import data from  file .'
    
    
    def add_arguments(self, parser):
        parser.add_argument('file_path',type=str,help='Path to the csv file.')
        parser.add_argument('model_name', type=str, help='Name of model .')
        
    def handle(self, *args, **kwargs):
    
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()
        # Search for model name 
        model = None
        for app_config in apps.get_app_configs():
            # try to search the model 
            try:
                model = apps.get_model(app_config.label, model_name)
                # break the loop
                break
            except LookupError:
                continue # model is not found in this app, continue searching for apps
        if not model:
            raise CommandError(f'Model {model_name} not found in any apps.')
        
        print('the file path is printed successfully.')
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            print(reader)
            for row in reader:
                print(row)
                # Student.objects.create(roll_no=row['roll_no'],name=row['name'],age=row['age'])
                # if there was a lot of data
                model.objects.create(**row)
        print(file_path)
        
        self.stdout.write(self.style.SUCCESS("Data imported from csv successfully."))
        
        # the running way is that python manage.py file path job_model 