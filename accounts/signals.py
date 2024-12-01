from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User, VolunteerUser, OrganizationUser
from django.db import transaction

@receiver(post_save, sender=User)
def create_or_update_related_user_profile(sender, instance, created, **kwargs):
    with transaction.atomic():
        # Create or update related profile for VolunteerUser
        if instance.role == 'volunteer':
            VolunteerUser.objects.get_or_create(user=instance)
        # Create or update related profile for OrganizationUser
        elif instance.role == 'organization':
            OrganizationUser.objects.get_or_create(user=instance)

@receiver(post_delete, sender=User)
def delete_related_user_profile(sender, instance, **kwargs):
    if instance.role == 'volunteer':
        VolunteerUser.objects.filter(user=instance).delete()
    elif instance.role == 'organization':
        OrganizationUser.objects.filter(user=instance).delete()
