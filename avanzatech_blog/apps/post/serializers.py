from rest_framework import serializers

from .models import Post, Comment, Like
from apps.user.serializer import UserSerializer, ShortUserSerializer


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
    updated_by = ShortUserSerializer(read_only=True)
    likes = LikeSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ['id','author','title','excerpt','created_at','updated_at',
                 'updated_by','comments','likes']

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author','title','content','public','authenticated','team','owner']


class EditPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['author','title','content','public','authenticated','team','owner']


