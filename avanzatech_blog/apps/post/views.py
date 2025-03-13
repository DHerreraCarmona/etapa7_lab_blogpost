from django.shortcuts import render

from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import PostSerializer, EditPostSerializer, CommentSerializer, LikeSerializer

from .models import Post, Comment, Like
from .pagination import PostListPagination, CommentsListPagination, LikeListPagination
from apps.user.models import CustomUser as Author
from .permissions import PostPermissions, filter_queryset_by_permissions



#View list of post ---------------------------------------------------------------------
class PostView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = PostSerializer
    pagination_class = PostListPagination

    def get_queryset(self):
        return filter_queryset_by_permissions(self.request, Post.objects.all(), PostPermissions)

    # def get_queryset(self):
    #     AllPost = Post.objects.all()
    #     allowed_posts=[]
    #     permission = PostPermissions()

    #     for post in AllPost:
    #         if permission.has_object_permission(self.request, self, post):
    #             allowed_posts.append(post)

    #     return Post.objects.filter(id__in=[post.id for post in allowed_posts]).distinct().order_by('created_at')
        

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
    queryset = Post.objects.all()
    permission_classes = [PostPermissions]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at = now())

#View list of comments ---------------------------------------------------------------------
class CommentsView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = CommentSerializer
    pagination_class = CommentsListPagination

    def get_queryset(self):
        return filter_queryset_by_permissions(self.request, Post.objects.all(), PostPermissions)
    

class CommentsPostView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = CommentSerializer
    pagination_class = CommentsListPagination
    def get_queryset(self):
        return filter_queryset_by_permissions(self.request, Post.objects.all(), PostPermissions)
    
    
    # def get_queryset(self):
    #     post_id = self.kwargs.get("pk")
    #     post = get_object_or_404(Post, id=post_id)  
    #     return Comment.objects.filter(post=post)

class CommentsAuthorView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = CommentSerializer
    pagination_class = CommentsListPagination

    def get_queryset(self):
        return filter_queryset_by_permissions(self.request, Post.objects.all(), PostPermissions)

    # def get_queryset(self):
    #     author_id = self.kwargs.get("id")
    #     author = get_object_or_404(Author, id=author_id)  
    #     return Comment.objects.filter(author=author)


#View list of Likes ---------------------------------------------------------------------

class LikesView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = LikeSerializer
    pagination_class = LikeListPagination

    def get_queryset(self):
        return filter_queryset_by_permissions(self.request, Post.objects.all(), PostPermissions)

class LikesPostView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = LikeSerializer
    pagination_class = LikeListPagination

    def get_queryset(self):
        return filter_queryset_by_permissions(self.request, Post.objects.all(), PostPermissions)
    
    # def get_queryset(self):
    #     post_id = self.kwargs.get("pk")
    #     post = get_object_or_404(Post, id=post_id)  
    #     return Like.objects.filter(post=post)

class LikesAuthorView(ListAPIView):
    allowed_methods = ['GET','HEAD','OPTIONS'] 
    serializer_class = LikeSerializer
    pagination_class = LikeListPagination

    def get_queryset(self):
        return filter_queryset_by_permissions(self.request, Post.objects.all(), PostPermissions)
    
    # def get_queryset(self):
    #     author_id = self.kwargs.get("id")
    #     author = get_object_or_404(Author, id=author_id)  
    #     return Like.objects.filter(author=author)

