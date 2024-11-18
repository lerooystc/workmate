from rest_framework.routers import DefaultRouter

from .views import BreedViewSet
from .views import DogViewSet


router = DefaultRouter()
router.register("dogs", DogViewSet, "cats")
router.register("breeds", BreedViewSet, "breeds")

urlpatterns = [] + router.urls
