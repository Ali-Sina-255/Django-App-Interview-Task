# i want to add some data in the database  using cusotm command .
from django.core.management.base import BaseCommand
from dataentery.models import Student

# Proposed command - python manage.py importdata file_path model_name
class Command(BaseCommand):
    help = 'It will insert data in to the database .'
    
    def handle(self, *args, **kwargs):
        # Add one single data 
        
        Student.objects.create(roll_no=1,name='ali',age=23)
        
        # Add mulityple data i
        dataset = [
            {'roll_no':2,'name':'Ali khan','age':23},
            {'roll_no':3,'name':'Khan Ali','age':23},
            {'roll_no':4,'name':'Jan Ali','age':24},
        ]
        
        for data in dataset:
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no=roll_no).exists()
            if not existing_record:
                Student.objects.create(roll_no=data['roll_no'],name=data['name'],age=data['age'])
            else:
                self.stdout.write(self.style.WARNING(f'Student with this {roll_no} is already exists!'))
        self.stdout.write(self.style.SUCCESS('Data inserted successfully in the database.'))
            