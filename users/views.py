from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserRegistrerSerializer
from .models import CustomUser

# User Register
class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrerSerializer
    permission_classes = [AllowAny]

# User view
class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user