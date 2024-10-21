from rest_framework import serializers
from .models import CustomUser
from follows.models import Follow
from django.core.cache import cache
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "first_name", "last_name", "followers_count"]
    
    def get_followers_count(self, obj):
        cache_key = f'user_followers_count_{obj.id}'
        followers_count = cache.get(cache_key)

        if followers_count is None:
            followers_count = Follow.objects.filter(following=obj).count()
            cache.set(cache_key, followers_count, timeout=settings.CACHE_TTL)

        return followers_count

class UserRegistrerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user