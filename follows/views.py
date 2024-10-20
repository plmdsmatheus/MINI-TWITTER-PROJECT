from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Follow, CustomUser
from .serializers import FollowSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_to_follow = CustomUser.objects.get(username=username)
        if request.user != user_to_follow:
            Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        return Response({'status': 'followed'})
    
    def delete(self, request, *args, **kwargs):
        user_to_unfollow = CustomUser.objects.get(username=username)
        Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
        return Response({'status': 'unfollowed'})