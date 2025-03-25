from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import UserPermission

#Create blogger and admins roles with migrate command 
@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if sender.name != "apps.user":  # Ensure this matches your actual app name
        return

    roles = [
        (0, "Blogger"),
        (1, "Admin"),
    ]

    for role_id, role_name in roles:
        UserPermission.objects.get_or_create(id=role_id, defaults={"role": role_id})