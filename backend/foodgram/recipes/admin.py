from django.contrib import admin

from recipes.models import Favorite
from recipes.models import Ingredient
from recipes.models import IngredientAmount
from recipes.models import Recipe
from recipes.models import ShoppingCart
from recipes.models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "color",
        "slug"
    )
    list_editable = (
        "name",
        "color",
        "slug"
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "measurement_unit"
    )
    list_editable = (
        "name",
        "measurement_unit"
    )
    list_filter = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "author",
        "name",
        "text",
        "cooking_time",
        "image",
        "pub_date"
    )
    list_editable = (
        "name",
        "cooking_time",
        "image",
        "author"
    )
    list_filter = (
        "name",
        "author"
    )


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "recipe",
        "ingredient",
        "amount"
    )
    list_editable = (
        "recipe",
        "ingredient",
        "amount"
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "recipe"
    )
    list_editable = (
        "user",
        "recipe"
    )


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "recipe"
    )
    list_editable = (
        "user",
        "recipe"
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
