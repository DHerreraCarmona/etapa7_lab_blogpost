from django.shortcuts import render

from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import PostSerializer, EditPostSerializer, CommentSerializer, LikeSerializer

from .models import Post, Comment, Like
from .pagination import CustomPagination
from apps.user.models import CustomUser as Author

#Pagination classes ---------------------------------------------------------------------

class PostListPagination(CustomPagination):
            page_size = 10

class CommentsListPagination(CustomPagination):
        page_size = 10

class LikeListPagination(CustomPagination):
    page_size = 20

#View list of post ---------------------------------------------------------------------
class PostView(ListAPIView):
        allowed_methods = ['GET','HEAD','OPTIONS'] 
        serializer_class = PostSerializer
        queryset = Post.objects.all()
        pagination_class = PostListPagination

#View create new post 
class CreatePostView(CreateAPIView):
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

#View list of comments ---------------------------------------------------------------------
class CommentsView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = CommentsListPagination

class CommentsPostView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = CommentSerializer
    pagination_class = CommentsListPagination
    
    def get_queryset(self):
        """Filtra los comentarios por el ID del post"""
        post_id = self.kwargs.get("pk")
        post = get_object_or_404(Post, id=post_id)  
        return Comment.objects.filter(post=post)

class CommentsAuthorView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = CommentSerializer
    pagination_class = CommentsListPagination

    def get_queryset(self):
        """Filtra los comentarios por el ID del post"""
        author_id = self.kwargs.get("id")
        author = get_object_or_404(Author, id=author_id)  
        return Comment.objects.filter(author=author)



#View list of comments ---------------------------------------------------------------------

class LikesView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    pagination_class = LikeListPagination

class LikesPostView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = LikeSerializer
    pagination_class = LikeListPagination
    
    def get_queryset(self):
        """Filtra los comentarios por el ID del post"""
        post_id = self.kwargs.get("pk")
        post = get_object_or_404(Post, id=post_id)  
        return Like.objects.filter(post=post)

class LikesAuthorView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = LikeSerializer
    pagination_class = LikeListPagination
    
    def get_queryset(self):
        """Filtra los comentarios por el ID del post"""
        author_id = self.kwargs.get("id")
        author = get_object_or_404(Author, id=author_id)  
        return Like.objects.filter(author=author)

