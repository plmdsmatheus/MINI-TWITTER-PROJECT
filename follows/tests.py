from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from posts.models import Post
from follows.models import Follow


class FollowIntegrationTest(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', password='password')
        self.user2 = CustomUser.objects.create_user(username='user2', password='password')
        self.client.login(username='user1', password='password')

    def test_follow_user_and_feed(self):
        # User1 follows User2
        url = f"/api/follows/follow/{self.user2.username}/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User2 creates a post
        self.client.logout()
        self.client.login(username='user2', password='password')
        Post.objects.create(user=self.user2, content="User2's post")

        # User1 should see User2's post in their feed
        self.client.logout()
        self.client.login(username='user1', password='password')
        url = "/api/posts/feed/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], "User2's post")
