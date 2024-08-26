from django.db import models
from django.conf import settings


STATUS_CHOICES = (
    ("Pending", "pending"),
    ("in-progress", "in-progress"),
    ("completed", "completed,"),
    ("failed", "failed),"),
)


class Job(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class JobResult(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    output = models.TextField(null=True)
    error_message = models.TextField(null=True)
    completed_at = models.DateTimeField(null=True)
