from rest_framework import serializers

from .models import Post, Comment, Like
from apps.user.serializer import UserSerializer, ShortUserSerializer

#Short serializers ---------------------------------------------------------------------
class ShortPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title']

class ShortCommentSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)
    content = serializers.CharField()
    class Meta:
        model = Comment
        fields = ['author','content','created_at']
        read_only_fields = ["author", "created_at"]

class ShortLikeSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['author']

#Post serializers -----------------------------------------------------------------------
class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    countLikes = serializers.SerializerMethodField()
    countComments = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','author','title','excerpt','created_at','countComments','countLikes']
    
    def get_author(self, obj):
        if obj.author is None:
            return None
        return {
            "id": obj.author.id,
            "username": obj.author.username,
            "team": obj.author.group.name if obj.author.group else "None"
    }

    def get_countLikes(self, obj):
        return obj.likes.count()
    
    def get_countComments(self, obj):
        return obj.comments.count()

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes = ShortLikeSerializer(read_only=True, many=True)
    comments = ShortCommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ['id','author','title','content','created_at','comments','likes']

class EditPostSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id','author','title','content','public','authenticated','team','owner']

#Detail Comments & Likes serializer ------------------------------------------------------
class DetailCommentSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)
    post = ShortPostSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['post','author','content','created_at']

class DetailLikeSerializer(serializers.ModelSerializer):
    author = ShortUserSerializer(read_only=True)
    post = ShortPostSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['post','author']