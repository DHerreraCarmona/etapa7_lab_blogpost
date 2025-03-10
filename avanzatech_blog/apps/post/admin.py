from django.contrib import admin
from .models import Post, Comment, Like

class PostAdmin(admin.ModelAdmin):
    list_display = ("title","author", "public", "created_at")
    exclude = ("excerpt", "slug", "updated_by")

class commentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")

class likeAdmin(admin.ModelAdmin):
    list_display = ( "post", "author", "created_at")

admin.site.register(Post, PostAdmin)
admin.site.register(Comment,commentAdmin)
admin.site.register(Like,likeAdmin)
