from rest_framework import serializers
from apps.user.serializer import UserSerializer, ShortUserSerializer
from .models import Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['author','content']

class LikeSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['author']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ['id','author','title','content',
                 'excerpt','created_at','updated_at',
                 'updated_by','slug','public','comments','likes']

