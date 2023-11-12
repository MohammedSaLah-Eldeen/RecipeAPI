"""
defines tests for the Tags API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse("recipe:tag-list")

def detail_url(tag_id):
    """returns tag detail URL."""
    return reverse("recipe:tag-detail", args=[tag_id])

def create_user(email='test@example.com', password='testpass123', name='example'):
    """creates and returns a user."""
    return get_user_model().objects.create_user(email=email, password=password, name=name)


class PublicTagsApiTests(TestCase):
    """Tests unauthorized API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """tests bad request when making requests."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Tests authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """tests retrieving tags list."""
        Tag.objects.create(user=self.user, name="15-min")
        Tag.objects.create(user=self.user, name="easy")

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """tests tags returned are for authenticated user."""
        user2 = create_user(email="test2@example.com", password="testpass123", name='test2')
        Tag.objects.create(user=user2, name="comfort-food")
        tag = Tag.objects.create(user=self.user, name="vegan")

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)




    

    

        