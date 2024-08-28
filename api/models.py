from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import UserProfile
User = get_user_model()



class Job(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.scheduled_time and self.scheduled_time < timezone.now():
            raise ValidationError("Jobs cannot be scheduled in the past.")

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def cancel(self):
        if self.status in ['pending', 'in_progress']:
            self.status = 'canceled'
            self.save()

    def is_completed(self):
        return self.status == 'completed'

    def __str__(self):
        return self.name


class JobResult(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    output = models.TextField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.job.status != 'completed':
            raise ValidationError("Results are only available for completed jobs.")


    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Result for {self.job.name}'


class Command(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]