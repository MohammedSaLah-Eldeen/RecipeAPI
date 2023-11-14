"""
serializers for the recipe API.
"""

from rest_framework import serializers
from core.models import *


class TagSerializer(serializers.ModelSerializer):
    """serializer for tags."""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_field = ["id"]


class IngredientSerializer(serializers.ModelSerializer):
    """serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ["id", "name"]
        read_only_field = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe."""

    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link", "tags", "ingredients"]
        read_only_fields = ["id"]

    def _get_or_create_tags(self, tags, recipe):
        """saves the list of tags to a specific recipe."""
        auth_user = self.context["request"].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        """saves a list of ingredients to a specific recipe."""
        auth_user = self.context["request"].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user, **ingredient
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """
        to create objects with this serializer that has
        a many-to-many field.
        because any model objects need serialization
        the many-to-many field which are db models
        needs serialization as well.

        django handles reading nested serializers but not creating
        so we needed to modify the create function.

        because passing data in serializer usually translates to
        direct values, related fields like many-to-many expect model objects
        not direct or raw like str or int values at all.

        this logic takes the raw input convert it to objects
        with the suitable serializer with the suitable model
        and then assign the related fields correctly.
        """
        tags = validated_data.pop("tags", [])
        ingredients = validated_data.pop("ingredients", [])
        recipe = Recipe.objects.create(**validated_data)  # unpack operator

        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        """
        handles updating for serializers with nested serializers
        to understand why there's a need for this
        check the create method.
        """
        # we sub with None as we want if the user
        # want to pass an empty list to remove all
        # the tags and ingredienst.
        tags = validated_data.pop("tags", None)
        ingredients = validated_data.pop("ingredients", None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        # normal updating.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # this is equivlant to instance.attr = value
            # because models are classes, we can pass values like this
        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """detail serializer for Recipe Serializer."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]

class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipe."""

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {
            'image': {
                'required': 'True',
            }
        }
