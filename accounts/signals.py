from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
	if created:
		print("user is created")
		UserProfile.objects.create(user=instance)
	else:
		try:
			profile = UserProfile.objects.get(user=instance)
			profile.save()
			print("user profile is updated")
		except:
			UserProfile.objects.create(user=instance)
			print("profile was not exist, but was created")
		print("user is updated")


# post_save.connect(post_save_create_profile_receiver)
@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
	print(instance.first_name + " " + "this user is being saved")