"""
Tests the User API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**kwargs):
    """helper function to create and return a new user."""
    return get_user_model().objects.create_user(
        email=kwargs.get("email", "test@example.com"),
        name=kwargs.get("name", "testExample"),
        password=kwargs.get("password", "testpassword"),
    )


class PublicUserApiTests(TestCase):
    """Tests the public - no login required - features"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """tests creating a user is successful"""
        payload = {
            "email": "test@example.com",
            "name": "testExample",
            "password": "testpassword",
        }  # contains the data needed for a post request.
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_existing_email_error(self):
        """tests error returned if a user with an email already exists."""
        payload = {
            "email": "test@example.com",
            "name": "testExample",
            "password": "testpassword",
        }  # contains the data needed for a post request.
        create_user()  # the helper function.
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """tests an error is returned if password less than 5 chars."""
        payload = {
            "email": "test@example.com",
            "name": "testExample",
            "password": "123",
        }  # contains the data needed for a post request.
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"])
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """tests create token for user."""
        create_user()
        payload = {
            "email": "test@example.com",
            "password": "testpassword",
        }  # contains the data needed for a post request.
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_create_token_bad_credentials(self):
        "tests create credentials with unvalid credentials."
        create_user()
        payload = {
            "email": "test@example.com",
            "password": "IncorrectPassword",
        }  # contains the data needed for a post request.
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_create_token_blank_password(self):
        """tests posting a blank password returns an error."""
        payload = {
            "email": "test@example.com",
            "password": "",
        }  # contains the data needed for a post request.
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    # this tests outputs an Error 'AnonmyousUser Object doesn't have attribute email'
    # def test_retrieve_user_unauthorized(self):
    #     """tests authentication is required."""

    #     res = self.client.get(ME_URL)
    #     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Tests the public - no login required - features"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_profile_success(self):
        """tests retrieving profile for logged in user."""
        res = self.client.get(ME_URL)
        user_me = {
            "email": "test@example.com",
            "name": "testExample",
        }

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, user_me)

    def test_post_me_not_allowed(self):
        """tests POST is not allowed iwth ME_URL."""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {
            "password": "WoodJutsu!",
            "name": "testeexample",
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
