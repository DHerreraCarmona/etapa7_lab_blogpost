from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, Like
from .filters import retrieve_obj
from .permissions import PostPermissions
from .pagination import CommentsListPagination, LikeListPagination
from .serializers import PostSerializer, ShortCommentSerializer, ShortLikeSerializer

#POST VIEWSET------------------------------------------------------------------------------------------------------------------
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    #Detail & Delete------------------------------------------------------------------------------
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,PostPermissions]

    def get_object(self):                                                          #Get Post                                
        post_id=self.kwargs["pk"]
        post = retrieve_obj(Post,post_id)
        if not PostPermissions().has_object_permission(self.request, self, post):
            raise NotFound({"error": "No Post matches the given query."})  
        return post

    def destroy(self, request, *args, **kwargs):                                   #Delete Post
        post_id=self.kwargs["pk"]
        post = retrieve_obj(Post,post_id)
        self.check_object_permissions(request, post)

        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    #Create Comments & Likes ------------------------------------------------------------------------
    @action( methods=["POST"], detail=True,                                        #Write Comments
            url_path="write-comment",
            serializer_class=ShortCommentSerializer,
            permission_classes=[PostPermissions])
    def write_comment(self,request,pk=None): 
        post = retrieve_obj(Post,pk)
        self.check_object_permissions(request, post)
        serializer = ShortCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action( methods=["POST"], detail=True,                                        #Give Like
            url_path="give-like",
            permission_classes=[PostPermissions])
    def give_like(self,request,pk):
        user = request.user
        post = retrieve_obj(Post,pk)
        self.check_object_permissions(request, post)
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
        post = retrieve_obj(Post,pk)
        if not PostPermissions().has_object_permission(request, self, post):
            raise NotFound({"error": "No Post matches the given query."}) 
        
        comments = post.comments.order_by("created_at")
        index = int(index) -1                                                          #Get comment by index not by comment id
        if index <0 or index >= comments.count():
            raise NotFound({"error": "No Post matches the given query."}) 
        comment = comments[index] 

        if request.method == "GET":                                                     #View comment
            serializer = self.get_serializer(comment)
            return Response(serializer.data)

        if request.method == "PATCH":                                                   #Edit comment
            if request.user != comment.author:
                raise NotFound({"error": "No Post matches the given query."}) 
            serializer = self.get_serializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == "DELETE":                                                  #Delete comment
            if request.user != comment.author:
                raise NotFound({"error": "No Post matches the given query."}) 
            comment.delete()
            return Response({"message": "comment deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)