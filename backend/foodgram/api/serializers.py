from recipes.models import Tag
from recipes.models import Ingredient
from recipes.models import Recipe
# from recipes.models import IngredientAmount

from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = "__all__"


class RecepSerializer(serializers.ModelSerializer):
    # author = serializers.SerializerMethodField()
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    ingredients = IngredientSerializer(
        many=True,
        read_only=True,
        source="recipes"
    )

    class Meta:
        model = Recipe
        fields = "__all__"