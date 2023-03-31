from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet
from api.views import TagViewSet
from api.views import RecepViewSet

app_name = "api"
router = DefaultRouter()

router.register(r"recipes", RecepViewSet, basename="recipes")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"ingredients", IngredientViewSet, basename="ingredients")
urlpatterns = [
    path("", include(router.urls)),
]
