from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

@api_view(['POST'])
def register_user(request):
    """
    Endpoint to handle user registration.
    """
    data = request.data
    if not data.get('username') or not data.get('email') or not data.get('password') or not data.get('role'):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if username or email already exists
    if User.objects.filter(username=data['username']).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=data['email']).exists():
        return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Create new user
    user = User.objects.create(
        username=data['username'],
        email=data['email'],
        role=data['role'],
        password=make_password(data['password']),
    )
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):
    """
    Endpoint to handle user login.
    """
    data = request.data
    if not data.get('username') or not data.get('password'):
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate user
    try:
        user = User.objects.get(username=data['username'])
        if user.check_password(data['password']):
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
