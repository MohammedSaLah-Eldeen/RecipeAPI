"""
Views for the Recipe API.
"""
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)

from core.models import *
from recipe.serializers import *

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='csv of tags'
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='csv of ingredients'
            )
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """Defines basic views for the recipe endpoint."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        modifies the default behaviour of getting all recipes
        to only recipes of the authenticated user.
        and filtering
        """
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset

        if tags:
            tag_names = tags.split(',')
            queryset = queryset.filter(tags__name__in=tag_names)

        if ingredients:
            ingredient_names = ingredients.split(',')
            queryset = queryset.filter(ingredients__name__in=ingredient_names)
        
        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()
        

    def get_serializer_class(self):
        """returns the needed serializer by default uses the one with description."""
        if self.action == "list":
            return RecipeSerializer
        elif self.action == 'upload_image':
            return RecipeImageSerializer

        return self.serializer_class
    
    @action(methods=['POST'], detail=True, url_path='upload_image')
    def upload_image(self, request, pk=None):
        """uploads an image to a recipe."""
        # refer to https://github.com/encode/django-rest-framework/blob/master/rest_framework/generics.py
        # line: 79 to understand how to it returns the correct object.
        recipe = self.get_object() 
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Manages tags in the database."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        modifies the default behaviour of getting all tags
        to only tags of the authenticated user.
        """
        return self.queryset.filter(user=self.request.user).order_by("-name")


class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Manages Ingredients in the database"""

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        modifies the normal behaviour of listing all ingredients
        to only list ingredients related to the user.
        """
        return self.queryset.filter(user=self.request.user).order_by("-name")
