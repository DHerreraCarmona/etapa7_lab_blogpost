# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.decorators import login_required

from .serializer import UserRegistrationSerializer
from .models import CustomUser

@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login exitoso'})
        else:
            return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
    else:
        return render(request, 'user/login.html')

def logout_view(request):
    logout(request)
    return redirect('login_page')

@login_required
def user_info(request):
    return JsonResponse({'username': request.user.username})

@api_view(["POST"])
@permission_classes([AllowAny]) 
@authentication_classes([TokenAuthentication])
@csrf_protect
def register_user(request): 
    queryset = CustomUser.objects.all()
    # data = request.data #if request.content_type == 'application/json' else request.POST
    serializer = UserRegistrationSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully","user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_protect
def register_page(request):
    return render(request, "user/register.html")