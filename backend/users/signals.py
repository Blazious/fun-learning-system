from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a profile when a new user is created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the user's profile when the user is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_delete, sender=Profile)
def delete_user_profile(sender, instance, **kwargs):
    """
    Handle profile deletion (though this shouldn't happen in normal operation).
    """
    # This is a safety measure in case a profile is accidentally deleted
    pass
