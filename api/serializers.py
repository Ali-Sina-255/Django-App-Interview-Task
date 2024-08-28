from rest_framework import serializers
from .models import Job, JobResult
from accounts.models import OTP, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.tasks import send_verification_email_task
from django.utils import timezone
import random


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'name', 'scheduled_time', 'status', 'created_at', 'updated_at']



class JobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResult
        fields = ['output', 'error_message', 'completed_at']



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        otp_code = str(random.randint(100000, 999999))
        otp_expiration = timezone.now() + timezone.timedelta(minutes=10)
        OTP.objects.create(user=user, otp_code=otp_code, expires_at=otp_expiration)

        
        email_template = "accounts/email/verification_email.html"
        domain = "localhost:8000"  
       
        send_verification_email_task.delay(user.id, otp_code, email_template, domain)

        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        return value


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = User.objects.get(email=attrs['email'])
        if not user.is_email_verified:
            raise serializers.ValidationError("Email is not verified.")
        return super().validate(attrs)


# {
    # "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNDg0MTA3NCwiaWF0IjoxNzI0NzU0Njc0LCJqdGkiOiIwMDgzYTY3OGYxZGU0MGRlOGZiMTNmMGNhMWRiMmRiOSIsInVzZXJfaWQiOjF9.0_QNqTbkSYksf4OamD7ksrWLxrRdftqltDa_yMoZcX8",
    # "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0NzU0OTc0LCJpYXQiOjE3MjQ3NTQ2NzQsImp0aSI6ImMwNDhmY2VjN2Y4NzRjYmZhMzczNGVkYzM0NjRjMGRmIiwidXNlcl9pZCI6MX0.SiyaH3vapZHDeeAtLZmw0N42N3pDmw-Xq-59byEeza8"
# }