from django.test import TestCase
from users.models import CustomUser
from posts.models import Post
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class PostModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user1', password='password')

    def test_create_post(self):
        post = Post.objects.create(user=self.user, content="Hello World")
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.content, "Hello World")

    def test_post_user(self):
        post = Post.objects.create(user=self.user, content="Hello World")
        self.assertEqual(post.user, self.user)

    def test_like_post(self):
        post = Post.objects.create(user=self.user, content="Hello World")
        post.likes.add(self.user)
        self.assertEqual(post.likes.count(), 1)
        self.assertEqual(post.likes.first(), self.user)


class PostAPITest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user1', password='password', email="user3@exemple.com")
        self.client.login(username='user1', password='password')

    def test_authenticate_user(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_create_post(self):
        self.authenticate_user()
        url = "/posts/"
        data = {"content": "This is my first post"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_get_posts(self):
        Post.objects.create(user=self.user, content="Test post")
        self.authenticate_user()
        url = "/posts/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)