from rest_framework import serializers
from .models import Post, Like

class PostSerializer(serializers.ModelSerializer):
    user = serializer.ReadOnlyField(source="user.username")

    class Meta:
        model = Post
        fields = ["id", "user", "content", "image", "created_at"]

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post", "liked_at"]