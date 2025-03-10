from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .viewsets import PostViewSet

router = DefaultRouter()
router.register('api',PostViewSet)

urlpatterns = [
    path('post/', views.create_post, name='create_post'),
    path('', views.post_list, name='post_list'),
    path('update_post/<int:pk>/', views.update_post, name='update_post'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),
] + router.urls