from django.db.models import Count
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Recipe)
from users.models import User


class UserGetSerializer(UserSerializer):
    """Сериализатор для пользователя, который возвращает
    дополнительное поле "is_subscribed",показывающее, подписан ли
    текущий пользователь на этого пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed"
        )

    def get_is_subscribed(self, obj):
        """Метод для получения значения поля "is_subscribed"."""

        subscriptions = self.context.get("subscriptions", set())
        return obj.id in subscriptions

class UserSerializer(UserCreateSerializer):
    """Сериализатор для создания и обновления объектов модели User."""

    first_name = serializers.CharField(
        required=True,
        allow_blank=False
    )
    last_name = serializers.CharField(
        required=True,
        allow_blank=False
    )
    email = serializers.EmailField(
        required=True,
        allow_blank=False
    )

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password"
        )


class SetPasswordSerializer(serializers.Serializer):
    """Сериализатор для обновления пароля пользователя."""

    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def update(self, instance, validated_data):
        """Обновление пароля пользователя. """

        if not instance.check_password(validated_data["current_password"]):

            raise serializers.ValidationError(
                {"current_password": f"Вы указали неправильный текущий пароль."
                                     f"проверти его: "
                                     f"{validated_data['current_password']}"}
            )

        if (validated_data["current_password"]
                == validated_data["new_password"]):

            raise serializers.ValidationError(
                {"new_password": "Ваш новый пароль должен отличаться "
                                 "от старого пароля"}
            )

        instance.set_password(validated_data["new_password"])
        instance.save()

        return validated_data


class CustomRecipeSerializer(serializers.ModelSerializer):
    """Список рецептов без ингридиентов."""
    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )


class SubscriptionsGetSerializer(serializers.ModelSerializer):
    """Серализатор для получения подписок пользователя"""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count"
        )

    def get_is_subscribed(self, obj):
        """Метод для получения значения поля "is_subscribed"."""

        subscriptions = self.context.get("subscriptions", set())
        return obj.id in subscriptions

    def get_recipes_count(self, obj):
        """Метод получает количество рецептов пользователя
        и возвращает его в виде целого числа"""

        qs = Recipe.objects.filter(author=obj).aggregate(count=Count("id"))

        return qs["count"]

    def get_recipes(self, obj):
        """Метод для получения рецептов пользователя
        и возврата их в сериализованном виде."""

        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        recipes = obj.recipes.all()

        if limit:
            recipes = recipes[:int(limit)]

        serializer = CustomRecipeSerializer(
            recipes,
            many=True,
            read_only=True
        )

        return serializer.data


class SubscriptionsSerializer(serializers.ModelSerializer):
    """Сериализатор подписок пользователей."""

    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = CustomRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count"
        )

    def get_is_subscribed(self, obj):
        """Метод для получения значения поля "is_subscribed"."""

        subscriptions = self.context.get("subscriptions", set())
        return obj.id in subscriptions

    def get_recipes_count(self, obj):
        """Метод получает количество рецептов пользователя
        и возвращает его в виде целого числа"""

        qs = Recipe.objects.filter(author=obj).aggregate(count=Count("id"))

        return qs["count"]
