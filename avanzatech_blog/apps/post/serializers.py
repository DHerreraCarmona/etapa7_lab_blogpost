from rest_framework import serializers
from apps.user.serializer import UserSerializer
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id','author','title','content',
                 'excerpt','created_at','updated_at',
                 'updated_by','slug','public']

