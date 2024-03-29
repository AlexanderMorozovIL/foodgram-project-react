from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import RecipeFilter
from api.permissions import OwnerOrReadOnly
from api.utils import generate_shopping_cart_text
from favorites.models import Favorite
from recipes.models import IngredientRecipe, Recipe
from shoppingcarts.models import ShoppingCart
from ..users.serializers import ShortRecipeSerializer
from .serializers import RecipeCreateSerializer, RecipeSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly, OwnerOrReadOnly)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if user.is_authenticated:
            if not Favorite.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                Favorite.objects.create(
                    user=user,
                    recipe=recipe
                )
                serializer = ShortRecipeSerializer(
                    recipe,
                    context={'request': request}
                )
                return Response(serializer.data)
            return Response(
                'Рецепт уже в избранном',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Требуется авторизация',
            status=status.HTTP_401_UNAUTHORIZED
        )

    @favorite.mapping.delete
    def remove_favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if user.is_authenticated:
            favorite = Favorite.objects.filter(
                user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response('Рецепт удалён из избранного')
            return Response(
                'Данный рецепт не в избранном',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Вы не авторизованы',
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if user.is_authenticated:
            if not ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                ShoppingCart.objects.create(user=user, recipe=recipe)
                serializer = ShortRecipeSerializer(
                    recipe,
                    context={'request': request})
                return Response(serializer.data)
            return Response(
                'Рецепт уже в вашем списке покупок',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Требуется авторизация',
            status=status.HTTP_401_UNAUTHORIZED
        )

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if user.is_authenticated:
            recipe_in_sopping_cart = ShoppingCart.objects.filter(
                user=user, recipe=recipe)
            if recipe_in_sopping_cart.exists():
                recipe_in_sopping_cart.delete()
                return Response('Рецепт удалён из списка покупок')
            return Response(
                'Данный рецепт не в списке покупок',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Вы не авторизованы',
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=self.request.user)
        recipes_in_shopping_cart = [item.recipe.id for item in shopping_cart]
        ingredients_to_buy = IngredientRecipe.objects.filter(
            recipe__in=recipes_in_shopping_cart).values('ingredient').annotate(
                amount=Sum('amount'))

        shopping_cart_text = generate_shopping_cart_text(ingredients_to_buy)

        return FileResponse(
            shopping_cart_text,
            content_type="text/plain",
            filename='shopping_cart.txt'
        )
