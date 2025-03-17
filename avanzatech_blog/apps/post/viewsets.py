from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

from .pagination import CommentsListPagination, LikeListPagination
from .serializers import PostSerializer, ShortCommentSerializer, ShortLikeSerializer
from .models import Post, Comment, Like
from .permissions import PostPermissions

#POST VIEWSET------------------------------------------------------------------------------------------------------------------
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    #Detail & Delete------------------------------------------------------------------------------
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    #pagination_class = PostListPagination
    permission_classes = [IsAuthenticatedOrReadOnly,PostPermissions]

    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs["pk"])
        if not PostPermissions().has_object_permission(self.request, self, post):
            raise Http404  
        return post

    def destroy(self, request, *args, **kwargs):                                   #Delete Post
        post = get_object_or_404(Post, pk=kwargs["pk"])
        self.check_object_permissions(request, post)

        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    #Create Comments & Likes ------------------------------------------------------------------------
    @action( methods=["POST"], detail=True,                                        #Write Comments
            url_path="write-comment",
            serializer_class=ShortCommentSerializer,
            permission_classes=[IsAuthenticated])
    def write_comment(self,request,pk=None):                                    
        user = request.user
        post = get_object_or_404(Post, id=pk)
        
        serializer = ShortCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action( methods=["POST"], detail=True,                                        #Give Like
            url_path="give-like",
            permission_classes=[IsAuthenticated] )
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
    
    #List Comments & Likes ------------------------------------------------------------------------------
    @action( methods=["GET"], detail=True, url_path="comments",                 #View Comment list 
            serializer_class = ShortCommentSerializer, 
            pagination_class = CommentsListPagination) 
    def view_comments(self,request,pk=None):                                                                       
        post = self.get_object()
        comments = post.comments.all()
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
    
    @action( methods=["GET"], detail=True, url_path="likes",                    #View Like list
            serializer_class = ShortLikeSerializer, 
            pagination_class = LikeListPagination)       
    def view_likes(self,request,pk=None):
        post = self.get_object()
        likes = post.likes.all()
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data)
    
    
#COMMENT VIEWSET----------------------------------------------------------------------------------------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    #List & Create Comments
    serializer_class = ShortCommentSerializer
    pagination_class = CommentsListPagination
    permission_classes = [IsAuthenticatedOrReadOnly,PostPermissions]
    
    #View,Edit & Delete specific comment------------------------------------------------------------
    @action( methods=["GET","PATCH","DELETE"], detail=True, url_path="comments/(?P<index>\\d+)")
    def view_comment(self,request,pk=None,index=None):
        post = get_object_or_404(Post, id=pk)
        if not PostPermissions().has_object_permission(request, self, post):
             return Response({"error": "No tienes permiso para ver este post."}, status=status.HTTP_404_NOT_FOUND)
        
        comments = post.comments.order_by("created_at")

        index = int(index) -1                                                          #Get comment by index not by comment id
        if index <0 or index >= comments.count():
            return Response(
                {"error": "Invalid index, comment not found"},status=status.HTTP_404_NOT_FOUND
            )
        comment = comments[index] 

        if request.method == "GET":                                                     #View comment
            serializer = self.get_serializer(comment)
            return Response(serializer.data)

        if request.method == "PATCH":                                                   #Edit comment
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

        if request.method == "DELETE":                                                  #Delete comment
            if request.user != comment.author:
                return Response(
                    {"error": "No tienes permiso para eliminar este post"},
                    status=status.HTTP_403_FORBIDDEN
                )
            comment.delete()
            return Response({"message": "comment deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)