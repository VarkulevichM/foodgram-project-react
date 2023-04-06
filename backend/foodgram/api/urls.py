from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet
from api.views import RecipeViewSet
from api.views import TagViewSet
from users.views import UserViewSet

app_name = "api"

router = DefaultRouter()
router.register(
    r"recipes",
    RecipeViewSet,
    basename="recipes"
)
router.register(
    r"tags",
    TagViewSet,
    basename="tags"
)
router.register(
    r"users",
    UserViewSet,
    basename="users"
)
router.register(
    r"ingredients",
    IngredientViewSet,
    basename="ingredients"
)

urlpatterns = [
    path(
        "",
        include(router.urls)
    ),
    path(
        r"auth/",
        include("djoser.urls.authtoken")
    ),
]
