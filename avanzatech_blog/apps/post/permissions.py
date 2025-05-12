from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from .models import Comment, Like

def same_team(user, post):
     return post.author.group == user.group

class PostPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        edit = request.method not in SAFE_METHODS

        if not user.is_authenticated:
            return not edit and obj.public
        if user.role.role == 1 or obj.author == user:
            return True
        
        if isinstance(obj, Comment) or isinstance(obj, Like):
            obj = obj.post 
        
        if not obj or not hasattr(obj, 'author') or not obj.author or not user or not hasattr(user, 'group'):
            is_team = False
        else:
            if (obj.author.group == "None" or user.group == "None"):
                is_team = False
            is_team = obj.author.group == user.group

        if getattr(view, "action", None) in ["give_like", "write_comment"]:
            return (obj.authenticated or (obj.team and is_team))
        
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
    