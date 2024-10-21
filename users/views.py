from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserRegistrerSerializer
from .models import CustomUser

# User Register
class UserRegisterView(generics.CreateAPIView):
    """
    post:
    Register a new user

    - Necessary fields: username, email, password
    - Login is not required
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrerSerializer
    permission_classes = [AllowAny]

# User view
class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    get:
    Get the current user's information

    - Login is required
    - Returns the user's id, username, email, first name, last name, and followers count

    put:
    Edit the current user's information (full update)

    - Necessary fields: username, email, first name, last name
    - Login is required
    - Only the user can edit their information

    patch:
    Edit the current user's information (partial update)

    - Necessary fields: username, email, first name, last name
    - Login is required
    - Only the user can edit their information
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user