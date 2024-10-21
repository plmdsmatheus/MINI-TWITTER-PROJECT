from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from .models import Follow, CustomUser
from .serializers import FollowSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

# Paginated list of followers and following
class FollowPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

# Follow and unfollow users in the API
class FollowUserView(APIView):
    """
    post:
    Follow a user by their username

    - Login is required
    - The user cannot follow themselves
    - Returns a status message if the user is followed

    delete:
    Unfollow a user by their username

    - Login is required
    - The user cannot follow themselves
    - Returns a status message if the user is unfollowed
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username, *args, **kwargs):
        user_to_follow = CustomUser.objects.get(username=username)
        if request.user != user_to_follow:
            Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
            cache.delete(f'user_followers_count_{user_to_follow.id}')
            cache.delete(f'user_following_count_{request.user.id}')
            return Response({'status': 'followed'})
        else:
            return Response({'status': 'You cannot follow yourself'})
    
    def delete(self, request, username, *args, **kwargs):
        user_to_unfollow = CustomUser.objects.get(username=username)
        Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
        cache.delete(f'user_followers_count_{user_to_unfollow.id}')
        cache.delete(f'user_following_count_{request.user.id}')
        return Response({'status': 'unfollowed'})

# List all followers of a user
class FollowersListView(generics.ListAPIView):
    """"
    get:
    List all followers of a user by their username with pagination

    - Login is required
    - Returns a paginated list of followers
    """

    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FollowPagination

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        return Follow.objects.filter(following=user)

# List all users that a user is following
class FollowingListView(generics.ListAPIView):
    """
    get:
    List all users that a user is following by their username with pagination

    - Login is required
    - Returns a paginated list of users that the user is following
    """

    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FollowPagination

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        return Follow.objects.filter(follower=user)