from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer

# Post list and create view
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Post edit and delete view
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
    
# Like and Unlike posts view
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs["pk"])
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
        return Response({"status": "liked" if created else "unliked"})
