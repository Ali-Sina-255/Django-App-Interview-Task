from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'name', 'scheduled_time', 'status', 'created_at', 'updated_at']

class JobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'result']
