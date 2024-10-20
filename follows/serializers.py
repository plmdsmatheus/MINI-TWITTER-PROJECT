from rest_framework import serializers
from .models import Follow

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source="follower.username")
    following = serializers.ReadOnlyField(source="following.username")

    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]