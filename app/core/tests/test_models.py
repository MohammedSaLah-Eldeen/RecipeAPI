"""
Models Tests.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import *
from decimal import Decimal

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

    def test_create_recipe(self):
        """tests creating a reciple is successful."""
        user = get_user_model().objects.create_user(
            email='Erza@mohammed.com',
            name='Erza Scarlet',
            password='kansoweaponchange!'
        )
        recipe = Recipe.objects.create(
            user=user,
            title='cake swords',
            time_minutes=15,
            price=Decimal('11.75'),
            description='beautiful and tasty cake in shape in swords.'
        )

        self.assertEqual(str(recipe), recipe.title)
