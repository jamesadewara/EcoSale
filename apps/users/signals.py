from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User, University


@receiver(post_save, sender=User)
def set_default_user_type(sender, instance, created, **kwargs):
    """
    Automatically set default values for new users after creation.
    """
    if created:
        # If no user_type is set, default to buyer
        if not instance.user_type:
            instance.user_type = 'buyer'
            instance.save()

        # You could send a welcome email here
        # Example (requires email backend configured):
        # from django.core.mail import send_mail
        # send_mail(
        #     'Welcome to our platform!',
        #     'Hi {}, welcome aboard!'.format(instance.full_name),
        #     settings.DEFAULT_FROM_EMAIL,
        #     [instance.email],
        #     fail_silently=True,
        # )


@receiver(post_save, sender=University)
def verify_university(sender, instance, created, **kwargs):
    """
    Perform any checks when a University is added/updated.
    For example: automatically mark as verified if in whitelist.
    """
    if created and instance.name.lower() in ["oxford university", "harvard university"]:
        instance.is_verified = True
        instance.save()
