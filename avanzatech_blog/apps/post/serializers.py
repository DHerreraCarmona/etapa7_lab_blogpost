from rest_framework import serializers

from .models import Post, Comment, Like
from apps.user.serializer import UserSerializer, ShortUserSerializer


#Comment serializer
class CommentSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['author','content']

#Like serializer
class LikeSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['author']

#Detail post serializer
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    updated_by = ShortUserSerializer(read_only=True)
    likes = LikeSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ['id','author','title','excerpt','created_at','updated_at',
                 'updated_by','comments','likes']

#Edit post serializer
class EditPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['author','title','content','public','authenticated','team','owner']


"""
#Create post serializer, now using only edit post
class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author','title','content','public','authenticated','team','owner']
"""