from recipes.models import Ingredient


def generate_shopping_cart_text(ingredients_to_buy):
    shopping_cart_text = 'Список покупок:\n'
    for item in ingredients_to_buy:
        ingredient = Ingredient.objects.get(pk=item['ingredient'])
        amount = item['amount']
        shopping_cart_text += (
            f'{ingredient.name}'
            f'({ingredient.measurement_unit}) - {amount}\n'
        )
    return shopping_cart_text
