from rest_framework import serializers
from .models import Job, JobResult, Command, Tag
from accounts.models import OTP, User, UserProfile
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



class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)


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
        model = UserProfile
        fields = ['profile_pic', 'address', 'state', 'city']
        extra_kwargs = {
            'address': {'required': False},
            'profile_pic': {'required': False},
            'state': {'required': False},
            'city': {'required': False},
        }

    def update(self, instance, validated_data):
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.address = validated_data.get('address', instance.address)
        instance.state = validated_data.get('state', instance.state)
        instance.city = validated_data.get('city', instance.city)

        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['first_name','last_name','email']

class CommandSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    job = JobSerializer() 

    class Meta:
        model = Command
        fields = ['id', 'owner', 'job', 'body', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'create_at']