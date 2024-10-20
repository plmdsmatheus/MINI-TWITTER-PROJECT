from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Follow, CustomUser
from .serializers import FollowSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

# Paginated list of followers and following
class FollowPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

# Follow and unfollow users in the API
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

# List all followers of a user
class FollowersListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FollowPagination

    def get_queryset(self):
        return Follow.objects.filter(following=self.kwargs['username'])

# List all users that a user is following
class FollowingListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FollowPagination

    def get_queryset(self):
        return Follow.objects.filter(follower=self.kwargs['username'])