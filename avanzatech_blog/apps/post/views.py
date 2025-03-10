from django.shortcuts import render

from rest_framework import status
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveUpdateDestroyAPIView, RetrieveAPIView

from .serializers import PostSerializer, EditPostSerializer, CreatePostSerializer
from .models import Post
from .pagination import CustomPagination

#View list of post
class ListPost(ListAPIView):
        allowed_methods = ['GET','HEAD','OPTIONS'] 
        serializer_class = PostSerializer
        queryset = Post.objects.all()

        class PostListPagination(CustomPagination):
            page_size = 3
        pagination_class = PostListPagination


#View create new post
class CreatePost(CreateAPIView):
        allowed_methods = ['POST'] 
        serializer_class = EditPostSerializer
        queryset = Post.objects.all()

        def perform_create(self, serializer):
            serializer.save(author=self.request.user)


#View edit a post
class EditPostView(RetrieveUpdateDestroyAPIView):
    allowed_methods = [ 'GET','PUT','DELETE','HEAD','OPTIONS']
    serializer_class = EditPostSerializer
    queryset = Post.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at = now())


#View detail post (now using a viewset)
class DetailPostView(RetrieveAPIView):
    allowed_methods = [ 'GET','HEAD','OPTIONS']
    serializer_class = PostSerializer
    queryset = Post.objects.all()
