from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharFiel(max_length=225)
    slug = models.SlugField(max_length=255, blank=True)
    content = models.TextField()
    excerpt = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=.models.SET_NULL, related_name="posts", null=False))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    class Permissions(models.TextChoices):  # 🔹 Definiendo opciones predefinidas
        READONLY = "RO", "Read Only"
        READEDIT = "RE", "Read & Edit"
        HIDDEN = "HD", "HIDDEN"

    Public = models.CharField(max_length=2,choices=Permissions.choices,default=Permissions.READONLY)
    Authenticated = models.CharField(max_length=2,choices=Permissions.choices,default=Permissions.READONLY)
    Team = models.CharField(max_length=2,choices=Permissions.choices,default=Permissions.READONLY)
    Owner = models.CharField(max_length=2,choices=Permissions.choices,default=Permissions.READEDIT)

    class Meta:
        ordering = ["-created_at"]