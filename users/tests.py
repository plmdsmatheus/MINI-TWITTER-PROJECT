from django.test import TestCase
from users.models import CustomUser
from posts.models import Post
from follows.models import Follow
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser


class UserModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="12345", email="user1@example.com")
        self.user2 = CustomUser.objects.create_user(username="testuser2", password="1pop5", email="user2@exemple.com")

    def test_user_creation(self):
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_user_data_create(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user2.username, "testuser2")

    def test_user_follow(self):
        follow = Follow.objects.create(follower=self.user, following=self.user2)
        self.assertEqual(Follow.objects.filter(following=self.user2).count(), 1)
        self.assertEqual(follow.follower, self.user)
        self.assertEqual(follow.following, self.user2)


class UserAPITest(APITestCase):

    def test_register_user(self):
        url = "/users/register/"
        data = {"username": "new_user", "password": "password123", "email": "newuser@example.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_login_user(self):
        self.user = CustomUser.objects.create_user(username='user1', password='password', email="newuser2@exemple.com")
        url = "/token/"
        data = {"username": "user1", "password": "password"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)