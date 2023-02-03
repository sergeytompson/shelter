from datetime import date

from django.contrib.auth.models import Group

from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from shelter_api.serializers import (
    PetsListSerializer,
    PetsDetailSerializer,
    PetsCrtUpdDelSerializer,
    ShelterUserRegistrationSerializer
)
from shelter_app.mixins import ShelterQuerysetMixin


class PetsViewSet(ShelterQuerysetMixin, ModelViewSet):
    permission_classes = [DjangoModelPermissions]

    def perform_create(self, serializer):
        if self.request.user.shelter is not None:
            serializer.save(shelter=self.request.user.shelter)
        else:
            raise ValidationError(
                "Пожалуйста, создайте новое животное в административной панели"
            )

    def get_serializer_class(self):
        if self.action == "list":
            return PetsListSerializer
        elif self.action == "retrieve":
            return PetsDetailSerializer
        else:
            return PetsCrtUpdDelSerializer

    def get_object(self):
        obj = super().get_object()
        birthday = obj.birthday
        today = date.today()
        age = (
            today.year
            - birthday.year
            - ((today.month, today.day) < (birthday.month, birthday.day))
        )
        obj.age = age
        return obj


class ShelterUserRegistrationAPIView(CreateAPIView):
    serializer_class = ShelterUserRegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.groups.add(Group.objects.get(name="guest"))
