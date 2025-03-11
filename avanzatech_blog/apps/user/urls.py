from django.urls import path, include
from . import views

urlpatterns = [
    #path('login/', views.login_view, name='login'),
    #path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_page, name='register_page'),
    path("api/register/", views.register_user, name="register_user"),
    path('api-auth/', include('rest_framework.urls')),
]

