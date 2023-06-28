from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscription

from .filters import RecipeFilter
from .pagination import CustomPagination
from .permissions import OwnerOrReadOnly
from .serializers import (AdvancedCustomUserSerializer, CustomUserSerializer,
                          IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          TagSerializer)

User = get_user_model()


class CustomUserViewSet(viewsets.ViewSet):
    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me'
    )
    def get_current_user_info(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk):
        if request.method == 'POST':
            following = get_object_or_404(User, id=pk)
            user = request.user
            if request.user == following:
                return Response('Вы не можете подписаться на самого себя')
            if user.is_authenticated:
                if not Subscription.objects.filter(
                        user=user,
                        following=following).exists():
                    Subscription.objects.create(
                        user=user,
                        following=following
                    )
                    serializer = AdvancedCustomUserSerializer(
                        following,
                        context={'request': request}
                    )
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        'Подписка уже оформлена',
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    'Требуется авторизация',
                    status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'DELETE':
            following = get_object_or_404(User, id=pk)
            user = request.user
            if user.is_authenticated:
                subscription = Subscription.objects.filter(
                    user=user, following=following)
                if subscription.exists():
                    subscription.delete()
                    return Response('Успешная отписка от пользователя')
                else:
                    return Response(
                        'Вы не можете отписаться от пользователя,'
                        ' на которого не были подписаны',
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    'Вы не авторизованы',
                    status=status.HTTP_401_UNAUTHORIZED)

    @action(
        detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        subscriptions = Subscription.objects.filter(user=request.user)
        users = [subscription.following for subscription in subscriptions]
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(users, request)
        users_serializer = AdvancedCustomUserSerializer(
            result_page,
            users,
            many=True,
            context={'request': request})
        users_serializer.is_valid()
        return paginator.get_paginated_response(users_serializer.data)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('name',)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly, OwnerOrReadOnly)

    def get_serializer_class(self):
        if self.action == 'create' and self.request.method == 'POST':
            return RecipeCreateSerializer
        elif self.action == 'update' and self.request.method == 'PATCH':
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
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
                else:
                    return Response(
                        'Рецепт уже в избранном',
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    'Требуется авторизация',
                    status=status.HTTP_401_UNAUTHORIZED
                )
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=pk)
            user = request.user
            if user.is_authenticated:
                favorite = Favorite.objects.filter(
                    user=user, recipe=recipe)
                if favorite.exists():
                    favorite.delete()
                    return Response('Рецепт удалён из избранного')
                else:
                    return Response(
                        'Данный рецепт не в избранном',
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    'Вы не авторизованы',
                    status=status.HTTP_401_UNAUTHORIZED)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
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
                else:
                    return Response(
                        'Рецепт уже в вашем списке покупок',
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    'Требуется авторизация',
                    status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=pk)
            user = request.user
            if user.is_authenticated:
                recipe_in_sopping_cart = ShoppingCart.objects.filter(
                    user=user, recipe=recipe)
                if recipe_in_sopping_cart.exists():
                    recipe_in_sopping_cart.delete()
                    return Response('Рецепт удалён из списка покупок')
                else:
                    return Response(
                        'Данный рецепт не в списке покупок',
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    'Вы не авторизованы',
                    status=status.HTTP_401_UNAUTHORIZED)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=self.request.user)
        recipes_in_shopping_cart = [item.recipe.id for item in shopping_cart]
        ingredients_to_buy = IngredientRecipe.objects.filter(
                recipe__in=recipes_in_shopping_cart
                ).values('ingredient').annotate(
                amount=Sum('amount')
            )

        shopping_cart_text = ''
        for item in ingredients_to_buy:
            ingredient = Ingredient.objects.get(pk=item['ingredient'])
            amount = item['amount']
            shopping_cart_text += (
                f'{ingredient.name}'
                f'({ingredient.measurement_unit}) - {amount}\n'
            )

        response = HttpResponse(shopping_cart_text, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shopping_cart.txt'
        )

        return response
