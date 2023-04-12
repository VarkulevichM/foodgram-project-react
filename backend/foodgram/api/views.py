import io

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import CustomSearchFilter
from api.filters import RecipeFilter
from api.pagination import CustomPaginator
from api.permissions import IsAuthorOrReadOnly
from api.serializers import IngredientSerializer
from api.serializers import RecipeCreateSerializer
from api.serializers import RecipeGetSerializer
from api.serializers import TagSerializer
from recipes.models import Favorite
from recipes.models import Ingredient
from recipes.models import IngredientAmount
from recipes.models import Recipe
from recipes.models import ShoppingCart
from recipes.models import Tag
from users.serializers import CustomRecipeSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Tag.
    Предоставляет возможности получения списка
    и детальной информации об тегов"""

    permission_classes = (AllowAny, )
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Ingredient.
    Предоставляет возможности получения списка
    и детальной информации об ингредиентах."""

    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (CustomSearchFilter, )


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Recipe. Предоставляет возможности просмотра,
    создания, изменения и удаления рецептов.
    Также позволяет добавлять рецепты в избранное, список покупок,
    а также скачивать список покупок.
    """

    queryset = Recipe.objects.all()
    pagination_class = CustomPaginator
    permission_classes = (IsAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Определяет сериализатор, используемый для конкретного метода."""

        if self.action in ("list", "retrieve"):
            return RecipeGetSerializer

        return RecipeCreateSerializer

    def get_serializer_context(self):
        """Определяет контекст сериализатора, включая список избранных
        рецептов и список рецептов в корзине покупок для аутентифицированных
        пользователей. Если пользователь не аутентифицирован, контекст не
        изменяется.
        """

        context = super().get_serializer_context()
        request = self.request

        if request and request.user.is_authenticated:
            favorites = set(
                Favorite.objects.filter(user=self.request.user)
                .values_list("recipe_id", flat=True)
            )
            context.update({"favorites": favorites})

            shopping_cart = set(
                ShoppingCart.objects.filter(user=self.request.user)
                .values_list("recipe_id", flat=True)
            )
            context.update({"shopping_cart": shopping_cart})

        return context

    @action(detail=True, methods=["post", "delete"],
            permission_classes=(IsAuthenticated,),
            url_path="favorite",
            url_name="favorite")
    def favorite(self, request, **kwargs):
        """Метод для добавления/удаления рецепта
        в список избранного у пользователя."""

        recipe = get_object_or_404(Recipe, id=kwargs["pk"])
        user = request.user

        if request.method == "POST":

            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"errors": "Рецепт уже добавлен в избранное"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            favorite = Favorite.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = CustomRecipeSerializer(favorite.recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            get_object_or_404(
                Favorite,
                user=user,
                recipe=recipe
            ).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=["post", "delete"],
            permission_classes=(IsAuthenticated,),
            url_path="shopping_cart",
            url_name="shopping_cart")
    def shopping_cart(self, request, **kwargs):
        """Позволяет добавлять и удалять рецепты в список покупок."""

        recipe = get_object_or_404(Recipe, id=kwargs["pk"])
        user = request.user

        if request.method == "POST":
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"errors": "Рецепт уже в списке покупок."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart = ShoppingCart.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = CustomRecipeSerializer(cart.recipe)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            get_object_or_404(
                ShoppingCart,
                user=user,
                recipe=recipe
            ).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=["get"],
            permission_classes=(IsAuthenticated,),
            url_path="download_shopping_cart",
            url_name="download_shopping_cart")
    def download_shopping_cart(self, request, **kwargs):
        """Позволяет скачивать список покупок в виде текстового файла."""

        ingredients = (
            IngredientAmount.objects
            .filter(recipe__shopping_recipe__user=request.user)
            .values("ingredient__name")
            .annotate(total_amount=Sum("amount"))
            .values_list(
                "ingredient__name",
                "total_amount",
                "ingredient__measurement_unit"
            )
        )

        buffer = io.BytesIO()

        with buffer:
            buffer.write("Список покупок\n\n".encode("utf-8"))

            for name, amount, unit in ingredients:
                buffer.write(f"{name} - {amount} {unit}.\n".encode("utf-8"))

            buffer.seek(0)
            response = HttpResponse(
                buffer.getvalue(),
                content_type="text/plain"
            )
            response[
                "Content-Disposition"] = "attachment; filename=shopping.txt"

            return response
