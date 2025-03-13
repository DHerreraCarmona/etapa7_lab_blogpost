from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class PostPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        edit = request.method not in SAFE_METHODS

        if not user.is_authenticated:
            return not edit and obj.public
        
        if user.role == 1 or obj.author == user:
            return True
        
        is_team = obj.author.groups.first() == user.groups.first()

        if obj.team and is_team:
            if obj.team == 1 and not edit : 
                    return True
            elif obj.team == 2:
                return True
            else: 
                 return False
            
        if not edit:
            return obj.authenticated

        return False 
    
def filter_queryset_by_permissions(request, queryset, permission_class):
    allowed_objects = []
    permission = permission_class()

    for obj in queryset:
        if permission.has_object_permission(request, None, obj):
            allowed_objects.append(obj)

    return queryset.filter(id__in=[obj.id for obj in allowed_objects]).distinct().order_by('created_at')
