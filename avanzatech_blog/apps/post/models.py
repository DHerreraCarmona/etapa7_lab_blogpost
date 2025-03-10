from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="posts", null=True)
    title = models.CharField(max_length=225)
    content = models.TextField()
    excerpt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="updated_post", null=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    
    class Permissions(models.TextChoices):
        READONLY = "RO", "Read Only"
        READEDIT = "RE", "Read & Edit"
        HIDDEN = "HD", "HIDDEN"

    public = models.CharField(max_length=2,choices=Permissions.choices,default=Permissions.READONLY)
    authenticated = models.CharField(max_length=2,choices=Permissions.choices,default=Permissions.READONLY)
    team = models.CharField(max_length=2,choices=Permissions.choices,default=Permissions.READONLY)
    owner = models.CharField(max_length=2,choices=Permissions.choices,default=Permissions.READEDIT)
    

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.excerpt = self.content[:199]
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            while Post.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f'{base_slug}-{num}'
                num += 1
            self.slug = slug

        super().save(*args, **kwargs)

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments", null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", null=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    Public = models.CharField(max_length=2,choices=Post.Permissions.choices,default=Post.Permissions.READONLY)
    """
    authenticated = models.CharField(max_length=2,choices=Post.Permissions.choices,default=Post.Permissions.READONLY)
    team = models.CharField(max_length=2,choices=Post.Permissions.choices,default=Post.Permissions.READONLY)
    owner = models.CharField(max_length=2,choices=Post.Permissions.choices,default=Post.Permissions.READEDIT)"""

    def __str__(self):
        return self.content

class Like(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes", null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    public = models.CharField(max_length=2,choices=Post.Permissions.choices,default=Post.Permissions.READONLY)
    """
    authenticated = models.CharField(max_length=2,choices=Post.Permissions.choices,default=Post.Permissions.READONLY)
    team = models.CharField(max_length=2,choices=Post.Permissions.choices,default=Post.Permissions.READONLY)
    owner = models.CharField(max_length=2,choices=Post.Permissions.choices,default=Post.Permissions.READEDIT)"""

    def __str__(self):
        return self.author.username
