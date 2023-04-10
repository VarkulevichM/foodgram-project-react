from django.core import validators
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель для ингредиентов которые используются в рецепте."""

    name = models.CharField(
        max_length=200,
        verbose_name="название"
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="единица измерения"
    )

    class Meta:
        ordering = ('name',)
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель для тегов которые используются в рецепте."""

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="название"
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name="цвет"

    )
    slug = models.SlugField(
        unique=True,
        verbose_name="slug"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Основная модель для рецептов"""

    name = models.CharField(
        max_length=255,
        verbose_name="название"
    )
    text = models.TextField(
        verbose_name="описание"
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="время приготовления",
        validators=(validators.MinValueValidator(1),)
    )
    image = models.ImageField(
        upload_to="recipe_images/",
        verbose_name="изображение"
    )
    pub_date = models.DateTimeField(
        verbose_name="дата публикации",
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="автор"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:20]


class IngredientAmount(models.Model):
    """Модель количества ингредиентов в рецепте"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="ингредиент"
    )
    amount = models.IntegerField(
        verbose_name="количество",
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "Ингредиенты для рецепта"
        verbose_name_plural = "Ингредиенты для рецепта"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_ingredient_amount"
            )
        ]

    def __str__(self):
        return f"{self.ingredient} - {self.recipe} {self.amount}"


class Favorite(models.Model):
    """Модель для избранного рецепта"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"],
                                    name="unique_favorite_recipes")
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class ShoppingCart(models.Model):
    """Модель для рецепта который будет добавлен в корзину"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipe',
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок"
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"],
                                    name="unique_cart_user_recipes")
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'
