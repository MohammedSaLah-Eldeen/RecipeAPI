"""
Urls for the Recipe endpoint.
"""

from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter
from recipe.views import *


router = DefaultRouter()
router.register("recipes", RecipeViewSet)
router.register("tags", TagViewSet)
router.register("ingredients", IngredientViewSet)

app_name = "recipe"
urlpatterns = [path("", include(router.urls))]
