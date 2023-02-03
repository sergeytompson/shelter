from django.urls import include, path
from rest_framework import routers

from .views import PetsViewSet, ShelterUserRegistrationAPIView

router = routers.SimpleRouter()
router.register(r"pet", PetsViewSet, basename="pet")
urlpatterns = [
    path("", include(router.urls)),
    path("auth", include("rest_framework.urls", namespace="rest_framework")),
    path("registration", ShelterUserRegistrationAPIView.as_view(), name="registration"),
]
