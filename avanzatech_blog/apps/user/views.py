# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication

from .serializer import UserRegistrationSerializer
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('success_page')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'user/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    # Redirect to a login page, home page, or any other page
    return redirect('user/login_page')

@api_view(["POST"])
@permission_classes([AllowAny]) 
@authentication_classes([TokenAuthentication])
def register_user(request):
    queryset = CustomUser.objects.all()
    data = request.data if request.content_type == 'application/json' else request.POST
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def register_page(request):
    return render(request, "user/register.html") 