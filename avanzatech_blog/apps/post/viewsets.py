from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .serializers import PostSerializer
from .models import Post

class PostListPagination(PageNumberPagination):
    page_size = 3

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]


    """@action(['GET'], detail=True, serializer_class=PostSerializer)
    def post_list(self,request,pk):
        posts = Post.objects.all()
        paginator = PostListPagination()
        paginated_posts = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)"""
        
    
    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated], url_path="post")
    def create_post(self, request):
        user = request.user
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user) 
        return Response(serializer.data)
    
    @action( methods=["POST"], detail=True, url_path="give-like")
    def give_like(self,request,pk):
        user = request.user
        post = get_object_or_404(Post, id=pk)
        msg = ""
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            msg = "Dislike"
        else:
            post.likes.add(user)
            msg = "like"
        post.save() 
        return Response({"status": f"{msg}"}, status=status.HTTP_200_OK)

"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])      #solo auth pueden crear post
def create_post(request):
    user = request.user
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
    return Response({"message: Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)"""