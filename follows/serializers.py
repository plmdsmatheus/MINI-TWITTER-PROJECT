from rest_framework import serializers
from .models import Follow
from users.models import CustomUser

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source="follower.username")
    following = serializers.ReadOnlyField(source="following.username")

    class Meta:
        model = Follow
        fields = ["follower", "following", "followed_at"]