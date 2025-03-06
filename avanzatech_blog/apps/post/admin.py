from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ("title","author", "public", "created_at")
    exclude = ("excerpt", "slug", "updated_by")


admin.site.register(Post, PostAdmin)