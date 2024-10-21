from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer
from rest_framework.pagination import PageNumberPagination
from follows.models import Follow
from django.core.cache import cache
from django.conf import settings

# Post list and create view
class PostListCreateView(generics.ListCreateAPIView):
    """
    get:
    List all posts in descending order of creation date

    - Login is required
    - Returns the id, user, content, image, and creation date of each post

    post:
    Create a new post

    - Necessary fields: content, image
    - Login is required
     
    """
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Post edit and delete view
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Get a post by its id

    - Login is required
    - Only the post's author can view it
    - Returns the id, user, content, creation date of the post, and the number of likes

    patch: 
    Edit a post by its id (partial update)
    
    - Necessary fields: content
    - Login is required
    - Only the post's author can edit it

    delete:
    Delete a post by its id

    - Login is required
    - Only the post's author can delete it

    put:
    Edit a post by its id (full update)

    - Necessary fields: content
    - Login is required
    - Only the post's author can edit it
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
    
# Like and Unlike posts view
class LikePostView(APIView):
    """
    post:
    Like a post by its id
    
    - Login is required
    - Returns a status message if the post is liked
    
    delete:
    Unlike a post by its id
    - Login is required
    - Returns a status message if the post is unliked
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs["pk"])
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
        return Response({"status": "liked" if created else "unliked"})
    
# Paginated post list view
class FeedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

# Feed view
class UserFeedView(generics.ListAPIView):
    """
    get:
    List all posts of users that the current user is following with pagination in descending order of creation date
    
    - Login is required
    - Returns the id, user, content, image, and creation date of each post
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user # Get the current user
        cache_key = f'user_feed_{user.id}' # Cache key for the feed
        feed = cache.get(cache_key) # Check if the feed is cached

        if not feed: # If the feed is not cached
            # Obtain the users that the current user is following
            following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
            # Obtain the posts of the users that the current user is following in descending order of creation
            feed = Post.objects.filter(user__in=following_users).order_by('-created_at')
            # Cache the feed
            cache.set(cache_key, feed, timeout=settings.CACHE_TTL)
        return feed
