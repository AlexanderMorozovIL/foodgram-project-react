from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'get_favorite_recipes_count'
    )
    list_filter = (
        'author',
        'name',
        'tags'
    )

    def get_favorite_recipes_count(self, obj):
        return obj.favorite_recipes.count()

    get_favorite_recipes_count.short_description = 'Добавлено в избранное'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = (
        'name',
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(IngredientRecipe)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
