from rest_framework import serializers
from .models import Post, Like

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    likes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ["user", "content", "image", "created_at", "likes_count"]
    
    def get_likes_count(self, obj):
        return Like.objects.filter(post=obj).count()

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["user", "post", "liked_at"]