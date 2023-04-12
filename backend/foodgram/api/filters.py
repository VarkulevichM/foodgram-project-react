from django_filters import rest_framework
from rest_framework import filters

from recipes.models import Recipe
from recipes.models import Tag


class RecipeFilter(rest_framework.FilterSet):
    """Класс фильтра для модели Recipe. Позволяет производить поиск рецептов
    по тегам, автору, наличию в списке избранного и корзине покупок.
    """

    tags = rest_framework.filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all()
    )
    is_favorited = rest_framework.filters.BooleanFilter(
        method="is_favorited_filter")
    is_in_shopping_cart = rest_framework.filters.BooleanFilter(
        method="is_in_shopping_cart_filter")

    class Meta:
        model = Recipe
        fields = ("tags", "author",)

    def is_favorited_filter(self, queryset, name, value):

        user = self.request.user

        if value and user.is_authenticated:
            return queryset.filter(favorite_recipe__user=user)

        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):

        user = self.request.user

        if value and user.is_authenticated:
            return queryset.filter(shopping_recipe__user=user)

        return queryset


class CustomSearchFilter(filters.SearchFilter):
    """Фильтр дли ингредиентов"""
    search_param = "name"
