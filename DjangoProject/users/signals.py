from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    """
    Creates the default profile after a new user is created.
    """
    if created:
        new = Profile.objects.create(user=instance)
        new.save()


@receiver(pre_delete, sender=get_user_model())
def delete_profile(sender, instance, **kwargs):
    """
    Deletes user profile picture when the account is deleted.
    """
    profile = Profile.objects.get(user=instance)
    if profile.image.name != 'default.jpg':
        profile.image.delete(False)
