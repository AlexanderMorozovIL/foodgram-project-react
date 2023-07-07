from rest_framework.viewsets import ReadOnlyModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from ingredients.models import Ingredient

from .serializers import IngredientSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)

    def get_queryset(self):
        name_starts_with = self.request.query_params.get(
            'name_starts_with', None
        )
        if name_starts_with:
            queryset = Ingredient.objects.filter(
                name__icontains=name_starts_with
            )
            return queryset.filter(name__icontains=name_starts_with)
        return super().get_queryset()
