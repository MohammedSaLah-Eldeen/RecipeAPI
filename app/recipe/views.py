"""
Views for the Recipe API.
"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe.serializers import *

class RecipeViewSet(viewsets.ModelViewSet):
    """Defines basic views for the recipe endpoint."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """modifies the default behaviour of getting all recipes
           to only recipes of the authenticated user.
        """
        return self.queryset.filter(user=self.request.user).order_by('-id')
    
    def get_serializer_class(self):
        """returns the needed serializer by default uses the one with description."""
        if self.action == 'list':
            return RecipeSerializer
        
        return self.serializer_class
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TagViewSet(mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    """Manages tags in the database."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """modifies the default behaviour of getting all tags
           to only tags of the authenticated user.
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')