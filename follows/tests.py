from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from posts.models import Post
from follows.models import Follow
from rest_framework_simplejwt.tokens import RefreshToken

class FollowIntegrationTest(APITestCase):

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', password='password', email='user1@example.com')
        self.user2 = CustomUser.objects.create_user(username='user2', password='password', email='user2@example.com')

    def authenticate_user(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_follow_user_and_feed(self):
        # user1 authenticate
        self.authenticate_user(self.user1)

        # User1 follows User2
        url = f"/follows/follow/{self.user2.username}/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # User2 create a post
        self.authenticate_user(self.user2)
        post = Post.objects.create(user=self.user2, content="User2's post")
        post.save()

        # Verify User2's post has created correctly
        self.assertEqual(Post.objects.count(), 1)

        # User1 in your feed can see User2's post
        self.authenticate_user(self.user1)
        url = "/posts/feed/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['content'], "User2's post")