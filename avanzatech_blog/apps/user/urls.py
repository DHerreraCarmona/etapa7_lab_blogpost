from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('rest_framework.urls')),
    path("csrf/", views.get_csrf),
    path("me/", views.user_info),
    path('register/', views.register_page, name='register_page'),
    path("user/register/", views.register_user, name="register_user"),
]

    