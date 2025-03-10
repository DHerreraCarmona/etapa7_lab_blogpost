from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .viewsets import PostViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet, basename="post")

urlpatterns = [
    path('post/', views.ListPost.as_view(), name='post_list'),
    path('blog/post/', views.CreatePost.as_view(), name='create_post'),
    path('blog/<int:pk>/', views.EditPostView.as_view(), name='edit_post'),
    #path('post/<int:pk>/', views.DetailPostView.as_view(), name='detail_post'),
    path("", include(router.urls)),
] #+ router.urls