from django.contrib import admin
from .models import Post, Comment, Like

class PostAdmin(admin.ModelAdmin):
    list_display = ("title","author", "created_at","updated_at","updated_by","public","authenticated","team","owner")
    readonly_fields = ("author", "updated_by", "created_at","updated_at")
    exclude = ("excerpt", "slug")

class commentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")
    readonly_fields = ("author","post","created_at")

class likeAdmin(admin.ModelAdmin):
    list_display = ( "post", "author", "created_at")
    readonly_fields = ("author","post")


admin.site.register(Post, PostAdmin)
admin.site.register(Comment,commentAdmin)
admin.site.register(Like,likeAdmin)
