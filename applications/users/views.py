from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_view(request):
    """Vista para el login de usuarios"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Crear o obtener token para el usuario
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'message': 'Login exitoso',
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Error en las credenciales',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_view(request):
    """Vista para el registro de usuarios"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        
        # Crear token para el nuevo usuario
        token = Token.objects.create(user=user)
        
        return Response({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Error en el registro',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    """Vista para el logout de usuarios"""
    if request.user.is_authenticated:
        # Eliminar el token del usuario
        Token.objects.filter(user=request.user).delete()
        logout(request)
        
        return Response({
            'success': True,
            'message': 'Logout exitoso'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Usuario no autenticado'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def user_profile(request):
    """Vista para obtener el perfil del usuario autenticado"""
    if request.user.is_authenticated:
        return Response({
            'success': True,
            'user': UserSerializer(request.user).data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Usuario no autenticado'
    }, status=status.HTTP_401_UNAUTHORIZED)
