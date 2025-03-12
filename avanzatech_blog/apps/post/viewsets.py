from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment, Like
from .permissions import PostPermissions

#POST VIEWSET----------------------------------------------------------------------------------------
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [PostPermissions]
    
    """def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        
        elif self.action == "list" or self.action == "retrieve":
            return [AuthPermissions()]
        
        elif self.action in ["update", "partial_update", "destroy"]:
            return [OwnerPermissions(), TeamPermissions()]
        
        return [IsAdminUser()]"""

    #Like
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
    
    #Comment
    @action( methods=["POST"], detail=True, url_path="write-comment",serializer_class=CommentSerializer)
    def write_comment(self,request,pk=None):
        user = request.user
        post = get_object_or_404(Post, id=pk)
        
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #View Comments list
    @action( methods=["GET"], detail=True, url_path="comments",serializer_class = CommentSerializer)
    def view_comments(self,request,pk=None):
        post = get_object_or_404(Post, id=pk)
        comments = post.comments.all()
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
    
    #Delete
    def destroy(self, request, *args, **kwargs):
        self.check_permissions(request)

        post = get_object_or_404(Post, pk=kwargs["pk"])
        post.delete()
        return Response({"message": "comment deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)
        

    
#COMMENT VIEWSET----------------------------------------------------------------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [PostPermissions]
    
    #View specific comment and modify
    @action( methods=["GET","PATCH","DELETE"], detail=True, url_path="comment/(?P<index>\\d+)")
    def view_comment(self,request,pk=None,index=None):
        post = get_object_or_404(Post, id=pk)
        comments = post.comments.order_by("created_at")
        index = int(index) -1
        
        if index <0 or index >= post.comments.count():
            return Response(
                {"error": "Invalid index, comment not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        comment = comments[index]                                   #Get comment by index
        
        #View comment
        if request.method == "GET":
            serializer = self.get_serializer(comment)
            return Response(serializer.data)

        #Edit comment
        if request.method == "PATCH":
            if request.user != comment.author:
                return Response(
                    {"error": "No tienes permiso para modificar este post"},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.get_serializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #Delete commemt
        if request.method == "DELETE":
            if request.user != comment.author:
                return Response(
                    {"error": "No tienes permiso para eliminar este post"},
                    status=status.HTTP_403_FORBIDDEN
                )
            comment.delete()
            return Response({"message": "comment deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)