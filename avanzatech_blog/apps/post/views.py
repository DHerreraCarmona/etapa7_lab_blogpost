from django.shortcuts import render
from django.utils.timezone import now
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveUpdateDestroyAPIView

from .models import Post, Comment, Like
from apps.user.models import CustomUser as Author
from .permissions import PostPermissions
from .filters import filter_posts, filter_reactions, retrieve_obj
from .pagination import PostListPagination, CommentsListPagination, LikeListPagination
from .serializers import PostSerializer, EditPostSerializer, ShortCommentSerializer, ShortLikeSerializer, DetailLikeSerializer, DetailCommentSerializer

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
        post_id = self.kwargs.get("pk")
        post = retrieve_obj(Post,post_id)
        
        if not PostPermissions().has_object_permission(self.request, self, post):
            raise NotFound({"error": "No Post matches the given query."}) 
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
    
class CommentsPostView(ListAPIView):                    # Buscar comentarios por post asociado
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailCommentSerializer
    pagination_class = CommentsListPagination

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = retrieve_obj(Post,post_id)
        
        if not PostPermissions().has_object_permission(self.request, self, post):
           raise NotFound({"error": "No Post matches the given query."}) 
        return filter_reactions(Comment, self.request, None, post_id)

class CommentsAuthorView(ListAPIView):                  # Buscar comentarios por autor
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailCommentSerializer
    pagination_class = CommentsListPagination

    def get_queryset(self):
        author_id = self.kwargs.get("author_id")        
        retrieve_obj(Author,author_id)
        return filter_reactions(Comment, self.request, author_id, None)

#View list of Likes ---------------------------------------------------------------------------
class LikesView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailLikeSerializer
    pagination_class = LikeListPagination

    def get_queryset(self):
        return filter_reactions(Like, self.request)

class LikesPostView(ListAPIView):                       # Buscar likes por post asociado
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailLikeSerializer
    pagination_class = LikeListPagination

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")      
        post = retrieve_obj(Post,post_id) 

        if not PostPermissions().has_object_permission(self.request, self, post):
           raise NotFound({"error": "No Post matches the given query."}) 
        return filter_reactions(Like, self.request, None, post_id)

class LikesAuthorView(ListAPIView):                     # Buscar likes por autor
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailLikeSerializer
    pagination_class = LikeListPagination

    def get_queryset(self):
        author_id = self.kwargs.get("author_id")  
        retrieve_obj(Author,author_id)
        return filter_reactions(Like, self.request, author_id, None)
