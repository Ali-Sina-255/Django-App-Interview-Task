from rest_framework import serializers
from .models import Job, JobResult
from accounts.models import OTP, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.tasks import send_verification_email_task
from accounts.utils import send_verification_email
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Q
import random

User = get_user_model()
class JobSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Job
        fields = ['id', 'name', 'price', 'scheduled_time', 'status', 'created_at', 'updated_at']



class JobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResult
        fields = ['output', 'error_message', 'completed_at']



class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
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



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate(self, data):
        email = data.get('email')
        first_name = data.get('first_name')
        
        if not first_name or not email:
            raise serializers.ValidationError('A first name and email are required to register.')
        
        User = get_user_model()
        user = User.objects.filter(email=email, first_name=first_name).distinct()
        if user.exists():
            raise serializers.ValidationError('This email or first name is already in use.')

        return data

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        
        # Send the verification email
        email_subject = 'Verify Your Email'
        email_template = 'accounts/email/verification_email.html'
        host = 'http://localhost:8000'  # Update this with your actual domain or host
        
        send_verification_email(user, email_subject, email_template, host)

        return user

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
        extra_kwargs = {
            'email': {'required': False},
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)

        instance.save()
        return instance

