from django.test import TestCase
from users.models import CustomUser
from posts.models import Post
from follows.models import Follow
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from django.core.exceptions import ValidationError


class UserModelTest(TestCase):

    def test_username_length_limit(self):
        user = CustomUser(username='a' * 21, email='user@example.com')
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_password_complexity(self):
        user = CustomUser(username='user1', password='simple', email='user1@example.com')
        with self.assertRaises(ValidationError): 
            user.full_clean() 

        user.set_password('Complex123!') 
        try:
            user.full_clean() 
        except ValidationError: 
            self.fail("") # This line should not be reached

class UserAPITest(APITestCase):

    def test_register_user(self):
        url = "/users/register/"
        data = {"username": "new_user", "password": "Password123!", "email": "newuser@example.com"}
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