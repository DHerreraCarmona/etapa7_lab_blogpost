from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Like

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    """
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    def retrieve(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)
        #serializer = self.get_serializer(post)
        likes_count = Like.objects.filter(post=post).count()
        user_has_liked = Like.objects.filter(post=post, author=request.user).exists() if request.user.is_authenticated else False

        return Response(
            {"post": post, "likes_count": likes_count, "user_has_liked": user_has_liked},
            template_name="post_detail.html",  # Usa la plantilla para renderizar HTML
        )
    """

    @action( methods=["POST"], detail=True, url_path="give-like")
    def give_like(self,request,pk):
        user = request.user
        post = get_object_or_404(Post, id=pk)
        like = Like.objects.filter(author=user, post=post).first()

        if like:
            like.delete()
            msg = "Dislike"
        else:
            Like.objects.create(author=user, post=post)
            msg = "Like"

        return Response({"status": msg}, status=status.HTTP_200_OK)
    
    @action( methods=["POST"], detail=True, url_path="write-comment",serializer_class=CommentSerializer)
    def write_comment(self,request,pk=None):
        user = request.user
        post = get_object_or_404(Post, id=pk)
        
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        """ Permite eliminar un post solo si el usuario es el autor """
        post = get_object_or_404(Post, pk=kwargs["pk"])
        
        if request.user != post.author:
            return Response(
                {"error": "No tienes permiso para eliminar este post"},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(request, *args, **kwargs)
