from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserPermission, Group

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email','id','username', 'is_staff', 'is_active', 'role', 'group') 
    list_filter = ('is_staff', 'is_active')                                             
    fieldsets = (
        (None, {'fields': ('email', 'username','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','role' ,'group', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email','username')                     
    ordering = ('email',)                                   

admin.site.register(CustomUser, CustomUserAdmin)               
admin.site.register(UserPermission)  
admin.site.register(Group) 

