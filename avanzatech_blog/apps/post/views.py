from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .serializers import PostSerializer
from .models import Post


@api_view(['POST'])
@permission_classes([IsAuthenticated])      #solo auth pueden crear post
def create_post(request):
    user = request.user
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostListPagination(PageNumberPagination):
    page_size = 3

@api_view(['GET'])
@permission_classes([AllowAny]) 
def post_list(request):
    posts = Post.objects.all()
    paginator = PostListPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(paginated_posts, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])  
#@authentication_classes([JWTAuthentication])
def update_post(request, pk):
    user = request.user 
    post = Post.objects.get(id=pk)
    if post.author != user:
        return Response({"error: You aren't the author"}, status=status.HTTP_403_FORBIDDEN)
    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  
#@authentication_classes([JWTAuthentication])
def delete_post(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    if post.author != user:
        return Response({"error: You aren't the author"}, status=status.HTTP_403_FORBIDDEN)
    post.delete()
    return Response({"message: Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)