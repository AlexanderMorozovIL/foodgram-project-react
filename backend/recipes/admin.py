from django.contrib import admin

from .models import IngredientRecipe, Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'get_favorite_recipes_count'
    )
    list_filter = (
        'author',
        'name',
    )
    filter_horizontal = (
        'tags',
    )

    @admin.display(description='Добавлено в избранное')
    def get_favorite_recipes_count(self, obj):
        return obj.favorite_recipes.count()


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )
