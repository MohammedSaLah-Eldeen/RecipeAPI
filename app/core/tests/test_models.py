"""
Models Tests.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    """Test Models"""

    def test_create_user_successful(self):
        """test creating a user"""
        email = "example@gmail.com"
        name = "example"
        password = "examplepassphrase"

        user = get_user_model().objects.create_user(
            email=email,
            name=name,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_no_email_error(self):
        """user without email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')