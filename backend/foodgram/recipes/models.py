from django.db import models
from users.models import User


class Tag(models.Model):
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="название"
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="единица измерения"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="автор"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="название"

    )
    image = models.ImageField(
        upload_to="recipe_images/",
        verbose_name="изображение"
    )
    text = models.TextField(
        verbose_name="описание"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientAmount"
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="теги"
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="время приготовления"
    )
    pub_date = models.DateTimeField(
        verbose_name="дата публикации",
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipes"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredients"
    )
    amount = models.PositiveIntegerField(
        verbose_name="количество"
    )

    class Meta:
        verbose_name = "Ингредиенты для рецепта"
        verbose_name_plural = "Ингредиенты для рецепта"

    def __str__(self):
        return f"{self.ingredient} - {self.recipe} {self.amount}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}"

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} - {self.recipe.name}"

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"


