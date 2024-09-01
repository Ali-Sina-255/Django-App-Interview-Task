from django.contrib import admin
from . models import Job, JobResult, Tag


admin.site.register(Job)
admin.site.register(JobResult)

admin.site.register(Tag)