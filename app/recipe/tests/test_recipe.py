"""
Tests the recipe API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Recipe
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer
)

from decimal import Decimal


def details_url(recipe_id):
    """creates and returns a recipe detail url."""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe_user(user, **kwargs):
    """create a sample recipe for a user."""
    defaults = {
        'title': 'TitleTest',
        'description': 'DescriptionTest',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'link': 'https://LinkTest.com/recipe.pdf'
    }
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


RECIPE_URL = reverse('recipe:recipe-list')


class PublicRecipeApiTest(TestCase):
    """Tests the recipe api no login features."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """authentication needed to call this api."""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Tests the recipe api login features."""

    def setUp(self):
        info = {
            'email': 'test@example.com',
            'name': 'testExample',
            'password': 'testtest123123'
        }
        self.user = get_user_model().objects.create_user(**info)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user) 

    def test_retrieve_recipes(self):
        """tests getting recipes list."""
        create_recipe_user(user=self.user)
        create_recipe_user(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_user_recipes(self):
        """tests getting recipes only related to user."""
        other_user = get_user_model().objects.create_user(
            'test@AnotherExample.com',
            'uwu',
            'uwuwuwuwu'
        )
        create_recipe_user(user=other_user)
        create_recipe_user(user=self.user)

        res = self.client.get(RECIPE_URL) 

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_get_recipe_detail(self):
        """tests get recipe detail."""
        recipe = create_recipe_user(user=self.user)
        url = details_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)


    def test_create_recipe(self):
        """tests creating recipe."""

        # note: we don't use our helper function
        # as it directly interacts with the database
        # to create a recipe, we test creating one
        # through a serializer.
        payload = {
            'title': 'daasdfafs',
            'time_minutes': 45,
            'price': Decimal('5')
        }
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
