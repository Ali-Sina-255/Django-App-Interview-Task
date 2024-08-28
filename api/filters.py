from django_filters.rest_framework import FilterSet
from . models import Job


class JobFilter(FilterSet):
	class Meta:
		model = Job
		fields = {
            'status': ['exact', 'in'],
            'name': ['icontains'],
            'description': ['icontains'],
        }