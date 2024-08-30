from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
	def create_user(self, first_name, last_name, email, password=None):
		if not email:
			raise ValueError("User must have an email address!")
	   
		user = self.model(
			email=self.normalize_email(email),
			first_name=first_name,
			last_name=last_name,
		)
		user.set_password(password)
		user.is_active = False 
		user.save(using=self._db)
		return user

	def create_superuser(self, first_name, last_name, email, password=None):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			first_name=first_name,
			last_name=last_name,
		)
		user.is_admin = True
		user.is_active = True  
		user.is_staff = True
		user.is_superadmin = True
		user.is_email_verified = True 
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255, unique=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False) 
	is_superadmin = models.BooleanField(default=False)
	is_email_verified = models.BooleanField(default=False) 

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["first_name", "last_name"]

	objects = UserManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)
	profile_pic = models.ImageField(upload_to="user/profile_picture", blank=True, null=True)
	address = models.CharField(max_length=200, null=True, blank=True)
	state = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.email


class OTP(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	otp_code = models.CharField(max_length=6)
	created_at = models.DateTimeField(auto_now_add=True)
	is_used = models.BooleanField(default=False)
	expires_at = models.DateTimeField()

	def clean(self):
		if self.expires_at < timezone.now():
			raise ValidationError("OTP has expired.")


		if OTP.objects.filter(user=self.user, otp_code=self.otp_code, is_used=False, expires_at__gt=timezone.now()).exists():
			raise ValidationError("An active OTP already exists for this user.")

	def save(self, *args, **kwargs):
		self.full_clean()  
		super().save(*args, **kwargs)

	def __str__(self):
		return f'OTP for {self.user.email}'