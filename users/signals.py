from djoser.signals import user_activated
from django.dispatch import receiver

@receiver(user_activated)
def activate_user(sender, user, request, **kwargs):
    user.is_verified = True
    user.save()
