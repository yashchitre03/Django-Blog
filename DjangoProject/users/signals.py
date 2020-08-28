from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    if created:
        new = Profile.objects.create(user=instance)
        new.save()


# @receiver(post_save, sender=get_user_model())
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()