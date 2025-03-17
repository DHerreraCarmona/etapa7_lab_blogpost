from django.http import Http404
from django.shortcuts import render

from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import PostSerializer, EditPostSerializer, ShortCommentSerializer, ShortLikeSerializer, DetailLikeSerializer, DetailCommentSerializer

from .models import Post, Comment, Like
from .pagination import PostListPagination, CommentsListPagination, LikeListPagination
from apps.user.models import CustomUser as Author
from .filters import filter_posts, filter_reactions
from .permissions import PostPermissions

#View list of post ------------------------------------------------------------------------------
class PostView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = PostSerializer
    pagination_class = PostListPagination

    def get_queryset(self):
        return filter_posts(Post, self.request)

#View create new post 
class CreatePostView(CreateAPIView):
    allowed_methods = ['POST'] 
    serializer_class = EditPostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)   

#View edit a post 
class EditPostView(RetrieveUpdateDestroyAPIView):
    allowed_methods = [ 'GET','PUT','DELETE','HEAD','OPTIONS']
    serializer_class = EditPostSerializer
    permission_classes = [PostPermissions]
    
    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs["pk"])
        if not PostPermissions().has_object_permission(self.request, self, post):
            raise Http404
        return post

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at = now())

#View list of comments ------------------------------------------------------------------------
class CommentsView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailCommentSerializer
    pagination_class = CommentsListPagination

    def get_queryset(self):
        return filter_reactions(Comment, self.request)
    
class CommentsPostView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailCommentSerializer
    pagination_class = CommentsListPagination
    def get_queryset(self):
        post_id = self.kwargs.get("post_id")      # Buscar comentarios por post asociado
        return filter_reactions(Comment, self.request, None, post_id)

class CommentsAuthorView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailCommentSerializer
    pagination_class = CommentsListPagination

    def get_queryset(self):
        author_id = self.kwargs.get("author_id")  # Buscar comentarios por autor
        return filter_reactions(Comment, self.request, author_id, None)

#View list of Likes ---------------------------------------------------------------------------
class LikesView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailLikeSerializer
    pagination_class = LikeListPagination

    def get_queryset(self):
        return filter_reactions(Like, self.request)

class LikesPostView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailLikeSerializer
    pagination_class = LikeListPagination

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")      # Buscar likes por post asociado
        return filter_reactions(Like, self.request, None, post_id)

class LikesAuthorView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailLikeSerializer
    pagination_class = LikeListPagination

    def get_queryset(self):
        author_id = self.kwargs.get("author_id")  # Buscar likes por autor
        return filter_reactions(Like, self.request, author_id, None)
