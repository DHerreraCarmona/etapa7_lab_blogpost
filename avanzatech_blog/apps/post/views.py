from django.shortcuts import render
from django.utils.timezone import now
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveUpdateDestroyAPIView

from .models import Post, Comment, Like
from .permissions import PostPermissions
from apps.user.models import CustomUser as Author
from .filters import filter_posts, filter_reactions, retrieve_obj
from .pagination import PostListPagination, CommentsListPagination, LikeListPagination
from .serializers import PostSerializer, EditPostSerializer, DetailLikeSerializer, DetailCommentSerializer

#View list of post ------------------------------------------------------------------------------
class PostView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = PostSerializer
    pagination_class = PostListPagination

    def get_queryset(self):
        return filter_posts(Post, self.request).order_by('-created_at')

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
        post = Post.objects.filter(id=self.kwargs["pk"]).first()
        
        if not PostPermissions().has_object_permission(self.request, self, post) or not self.request.user.is_authenticated or not post:
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
    
class CommentsPostView(ListAPIView):                    # Search comments by post id
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailCommentSerializer
    pagination_class = CommentsListPagination

    def get_queryset(self):
        post = retrieve_obj(Post,self.kwargs.get("post_id"))
        return filter_reactions(Comment, self.request, None, post_id=post.id)

class CommentsAuthorView(ListAPIView):                  # Search comments by author id
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailCommentSerializer
    pagination_class = CommentsListPagination

    def get_queryset(self):
        author=retrieve_obj(Author,self.kwargs.get("author_id"))
        return filter_reactions(Comment, self.request, author_id=author.id)

#View list of Likes ---------------------------------------------------------------------------
class LikesView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailLikeSerializer
    pagination_class = LikeListPagination

    def get_queryset(self):
        return filter_reactions(Like, self.request)

class LikesPostView(ListAPIView):                       # Search likes by post id
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailLikeSerializer
    pagination_class = LikeListPagination

    def get_queryset(self):
        post = retrieve_obj(Post,self.kwargs.get("post_id")) 
        return filter_reactions(Like, self.request, None, post_id=post.id).order_by("-created_at")

class LikesAuthorView(ListAPIView):                     # Search comments by author id
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = DetailLikeSerializer
    pagination_class = LikeListPagination

    def get_queryset(self):
        author=retrieve_obj(Author,self.kwargs.get("author_id"))
        return filter_reactions(Like, self.request, author_id=author.id)
