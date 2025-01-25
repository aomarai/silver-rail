from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class UserRegistrationTests(APITestCase):
    """
    Test suite for user registration functionality.
    """
    register_url = reverse('register')

    def test_valid_user_registration(self):
        """
        Ensure a user can register with valid data.
        """
        url = self.register_url
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'testuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_missing_username_registration(self):
        """
        Ensure registration fails if the username is missing.
        """
        url = self.register_url
        data = {'password': 'testpassword', 'email': 'testuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_password_registration(self):
        """
        Ensure registration fails if the password is missing.
        """
        url = self.register_url
        data = {'username': 'testuser', 'email': 'testuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_email_registration(self):
        """
        Ensure registration fails if the email is missing.
        """
        url = self.register_url
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_username_registration(self):
        """
        Ensure registration fails if the username already exists.
        """
        User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        url = self.register_url
        data = {'username': 'testuser', 'password': 'newpassword', 'email': 'newemail@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class JWTAuthenticationTests(APITestCase):
    """
    Test suite for JWT authentication functionality.
    """
    obtain_pair_url = reverse('login')
    refresh_token_url = reverse('refresh')

    def test_valid_token_obtain_pair(self):
        """
        Ensure a valid token pair can be obtained with correct credentials.
        """
        User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        url = self.obtain_pair_url
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_token_obtain_pair(self):
        """
        Ensure token pair cannot be obtained with incorrect credentials.
        """
        User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        url = self.obtain_pair_url
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_token_refresh(self):
        """
        Ensure a valid access token can be obtained with a valid refresh token.
        """
        User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        url = self.obtain_pair_url
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        refresh_token = response.data['refresh']

        url = self.refresh_token_url
        data = {'refresh': refresh_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_invalid_token_refresh(self):
        """
        Ensure access token cannot be obtained with an invalid refresh token.
        """
        url = self.refresh_token_url
        data = {'refresh': 'invalidtoken'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)