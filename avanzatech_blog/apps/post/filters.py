from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import NotFound

from .permissions import PostPermissions

def filter_posts(model,request):
    queryset = model.objects.all()
    permission = PostPermissions()
    allowed_obj = []

    for obj in queryset:
        if permission.has_object_permission(request, None, obj):
            allowed_obj.append(obj)

    return queryset.filter(id__in=[obj.id for obj in allowed_obj]).distinct().order_by('created_at')

def filter_reactions(model, request, author_id=None, post_id=None):
    queryset = model.objects.all()
    permission = PostPermissions()
    allowed_obj = []

    if author_id:
        queryset = queryset.filter(author__id=author_id)

    elif post_id and hasattr(model, 'post'):
        queryset = queryset.filter(post__id=post_id)

    for obj in queryset:
        if permission.has_object_permission(request, None, obj.post):
            allowed_obj.append(obj.id)

    return model.objects.filter(id__in=allowed_obj).distinct().order_by('post_id')

def retrieve_obj(Model,obj_id):
    if obj_id is None:
        raise NotFound({"error": "No Post matches the given query."}) 
    
    try:
        obj = Model.objects.get(pk=obj_id)
    except Model.DoesNotExist or not obj:
        raise NotFound({"error": "No Post matches the given query."}) 
    return obj