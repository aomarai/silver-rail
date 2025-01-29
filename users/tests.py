from django.urls import reverse
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.settings import api_settings


from users.models import SilverRailUser

TEST_REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "registration": "40/second",
        "anon": "100/day",
        "user": "1500/day",
        "burst": "60/min",
        "sustained": "1000/day"
    },
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle"
        "rest_framework.throttling.UserRateThrottle",
    ],
}

@override_settings(REST_FRAMEWORK=TEST_REST_FRAMEWORK)
class UserRegistrationTests(APITestCase): # TODO: Get the rate limiting on the user registration tests working
    """
    Test suite for user registration functionality.
    """
    register_url = reverse("register")

    def test_valid_user_registration(self):
        """
        Ensure a user can register with valid data.
        """
        url = self.register_url
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "testuser@example.com",
        }
        print(api_settings.DEFAULT_THROTTLE_RATES)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SilverRailUser.objects.count(), 1)
        self.assertEqual(SilverRailUser.objects.get().username, "testuser")

    def test_missing_username_registration(self):
        """
        Ensure registration fails if the username is missing.
        """
        url = self.register_url
        data = {"password": "testpassword", "email": "testuser@example.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_password_registration(self):
        """
        Ensure registration fails if the password is missing.
        """
        url = self.register_url
        data = {"username": "testuser", "email": "testuser@example.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_email_registration(self):
        """
        Ensure registration fails if the email is missing.
        """
        url = self.register_url
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_username_registration(self):
        """
        Ensure registration fails if the username already exists.
        """
        SilverRailUser.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        url = self.register_url
        data = {
            "username": "testuser",
            "password": "newpassword",
            "email": "newemail@example.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email_registration(self):
        """
        Ensure registration fails if the email already exists.
        """
        SilverRailUser.objects.create_user(
            username="testuser1", password="testpassword", email="testuser@example.com"
        )
        url = self.register_url
        data = {
            "username": "testuser2",
            "password": "newpassword",
            "email": "testuser@example.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_username_registration(self):
        """
        Ensure registration fails if the username already exists.
        """
        SilverRailUser.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        url = self.register_url
        data = {
            "username": "testuser",
            "password": "newpassword",
            "email": "newemail@example.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_limiting_registration(self):
        """
        Ensure rate limiting is applied to registration.
        """
        url = self.register_url

        max_registrations = int(TEST_REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["registration"][:2])

        for i in range(max_registrations):
            data = {
                "username": f"testuser{i}",
                "password": "testpassword",
                "email": f"testuser{i}@example.com",
            }
            self.client.post(url, data, format="json")

        data = {
            "username": "testuser-shouldntexist",
            "password": "testpassword",
            "email": "testuser-shouldntexist@example.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class JWTAuthenticationTests(APITestCase):
    """
    Test suite for JWT authentication functionality.
    """

    obtain_pair_url = reverse("login")
    refresh_token_url = reverse("refresh")

    def test_valid_token_obtain_pair(self):
        """
        Ensure a valid token pair can be obtained with correct credentials.
        """
        SilverRailUser.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        url = self.obtain_pair_url
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_token_obtain_pair(self):
        """
        Ensure token pair cannot be obtained with incorrect credentials.
        """
        SilverRailUser.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        url = self.obtain_pair_url
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_token_refresh(self):
        """
        Ensure a valid access token can be obtained with a valid refresh token.
        """
        SilverRailUser.objects.create_user(
            username="testuser", password="testpassword", email="testuser@example.com"
        )
        url = self.obtain_pair_url
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        refresh_token = response.data["refresh"]

        url = self.refresh_token_url
        data = {"refresh": refresh_token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_invalid_token_refresh(self):
        """
        Ensure access token cannot be obtained with an invalid refresh token.
        """
        url = self.refresh_token_url
        data = {"refresh": "invalidtoken"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
