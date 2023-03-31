from rest_framework import mixins
from rest_framework import viewsets

from api.serializers import IngredientSerializer
from api.serializers import RecepSerializer
from api.serializers import TagSerializer
from recipes.models import Ingredient
from recipes.models import Recipe
from recipes.models import Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecepViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecepSerializer
