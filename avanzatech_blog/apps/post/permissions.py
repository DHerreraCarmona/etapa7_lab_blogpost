from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class PostPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return request.method in SAFE_METHODS and obj.public

        if user.role == 1 or obj.author == user:
            return True
        
        edit = request.method not in SAFE_METHODS
        is_team = obj.author.groups.first() == request.user.groups.first()

        if is_team:
            if obj.team == 1 and not edit :
                    return True
            elif obj.team == 2 and edit:
                return True
            else: 
                 return False
            
        if not edit:
            return request.method in SAFE_METHODS and obj.authenticated
                
        return False