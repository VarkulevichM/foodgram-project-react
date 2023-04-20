from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient
from recipes.models import IngredientAmount
from recipes.models import Recipe
from recipes.models import Tag
from users.serializers import UserGetSerializer


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ingredient для всех полей."""

    class Meta:
        model = Ingredient
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tag для всех полей."""

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientAmountGETSerializer(serializers.ModelSerializer):
    """Список ингредиентов с количеством для рецепта."""

    id = serializers.ReadOnlyField(
        source="ingredient.id"
    )
    name = serializers.ReadOnlyField(
        source="ingredient.name"
    )
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientAmount
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount"
        )


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения рецепта."""

    author = UserGetSerializer(
        read_only=True
    )
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    ingredients = IngredientAmountGETSerializer(
        many=True,
        read_only=True,
        source="recipes"
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = "__all__"

    def get_is_favorited(self, obj):
        """Возвращает True, если рецепт в избранном у пользователя,
        иначе False."""

        if "favorites" in self.context:
            return obj.id in self.context["favorites"]

        return False

    def get_is_in_shopping_cart(self, obj):
        """Возвращает True, если рецепт в списке покупок у пользователя,
        иначе False."""

        if "shopping_cart" in self.context:
            return obj.id in self.context["shopping_cart"]

        return False


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов рецепта."""

    id = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = (
            "id",
            "amount"
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сереализатор создания, удаления и обновления рецепта"""

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    author = UserGetSerializer(
        read_only=True
    )
    id = serializers.ReadOnlyField()
    ingredients = RecipeIngredientSerializer(
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
            "author"
        )

    def validate(self, obj):

        if not obj.get("tags"):
            raise serializers.ValidationError(
                "Хотя бы один тег должен быть указан в tags"
            )
        if not obj.get("ingredients"):
            raise serializers.ValidationError(
                "Хотя бы один ингредиент должен быть указан в ingredients"
            )

        return obj

    def tags_and_ingredients_set(self, recipe, tags, ingredients):
        """Устанавливает связь многие-ко-многим с моделью
        Tag и RecipeIngredient для экземпляра рецепта."""

        recipe.tags.set(tags)
        IngredientAmount.objects.bulk_create(
            [IngredientAmount(
                recipe=recipe,
                ingredient=Ingredient.objects.get(pk=ingredient["id"]),
                amount=ingredient["amount"]
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        """Создает новый объект рецепта."""

        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        recipe = Recipe.objects.create(author=self.context["request"].user,
                                       **validated_data)
        self.tags_and_ingredients_set(recipe, tags, ingredients)
        return recipe

    def update(self, instance, validated_data):
        """Обновляет существующий объект рецепта."""

        instance.image = validated_data.get("image", instance.image)
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time",
            instance.cooking_time
        )
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        IngredientAmount.objects.filter(
            recipe=instance,
            ingredient__in=instance.ingredients.all()).delete()

        self.tags_and_ingredients_set(instance, tags, ingredients)
        instance.save()

        return instance

    def to_representation(self, instance):
        return RecipeGetSerializer(instance,
                                   context=self.context).data
