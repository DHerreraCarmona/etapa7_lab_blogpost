from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Permissions

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id','email','username', 'is_staff', 'is_active', 'role')  # Campos visibles en la lista de usuarios
    list_filter = ('is_staff', 'is_active')  # Filtros en el admin
    fieldsets = (
        (None, {'fields': ('email', 'username','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','role' ,'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email','username')  # Permite buscar por email en el admin
    ordering = ('email',)  # Ordena por email

admin.site.register(CustomUser, CustomUserAdmin)  # Registra el modelo en el admin
admin.site.register(Permissions)  # Registra el modelo en el admin

