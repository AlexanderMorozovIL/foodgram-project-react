from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from recipes.models import Recipe
from users.models import Subscription

# from ..subrecipes.recipes_serializers import ShortRecipeSerializer


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователей с дополнительной валидацией."""
    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me".'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return value

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели CustomUser."""
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, following=obj).exists()


class AdvancedCustomUserSerializer(CustomUserSerializer):
    """Расширенный сериализатор для модели CustomUser."""
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta(CustomUserSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            recipes = Recipe.objects.filter(author=obj)
            serializer = ShortRecipeSerializer(
                recipes,
                many=True,
                context={'request': request}
            )
            return serializer.data
        return []

    def get_recipes_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Recipe.objects.filter(author=obj).count()
        return 0


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого представления рецепта."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
