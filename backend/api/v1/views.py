from recipe.models import Ingredient, Tag, Recipe

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
