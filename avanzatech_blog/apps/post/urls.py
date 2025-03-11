from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .viewsets import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet, basename="post")

urlpatterns = [
    path('post/', views.PostView.as_view(), name='post_list'),
    path('likes/', views.LikesView.as_view(), name='comments_list'),
    path('comments/', views.CommentsView.as_view(), name='comments_list'),
    path('blog/<int:pk>/', views.EditPostView.as_view(), name='edit_post'),
    path('post/create/', views.CreatePostView.as_view(), name='create_post'),
    path('likes/post/<int:pk>/', views.LikesPostView.as_view(), name='comments_list'),
    path('likes/author/<int:id>/', views.LikesAuthorView.as_view(), name='comments_list'),
    path('comments/post/<int:pk>/', views.CommentsPostView.as_view(), name='comments_list'),
    path('comments/author/<int:id>/', views.CommentsAuthorView.as_view(), name='comments_list'),
    path("", include(router.urls)),

    path("post/<int:pk>/comments/<int:index>/", CommentViewSet.as_view({
        "get": "view_comment",
        "patch": "view_comment",
        "delete": "view_comment"
    }), name="comment_detail"),
]