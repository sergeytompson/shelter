from typing import Type, TypeVar

from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from shelter.settings import READ_GROUP_NAME
from shelter_api.serializers import (PetsCreateSerializer,
                                     PetsDeleteSerializer,
                                     PetsDetailSerializer, PetsListSerializer,
                                     PetsUpdateSerializer,
                                     ShelterUserRegistrationSerializer)
from shelter_app.mixins import ShelterQuerysetMixin
from shelter_app.models import Pets
from utils.birthday_to_age import convert_birthday_to_age

T = TypeVar("T", bound=serializers.ModelSerializer)


class PetsViewSet(ShelterQuerysetMixin, ModelViewSet):
    permission_classes = (DjangoModelPermissions,)

    def perform_create(self, serializer: Type[T]) -> None:
        if self.request.user.shelter is not None:
            serializer.save(shelter=self.request.user.shelter)
        else:
            raise ValidationError(
                "Пожалуйста, создайте новое животное в административной панели"
            )

    def get_serializer_class(self) -> Type[T]:
        match self.action:
            case "list":
                return PetsListSerializer
            case "retrieve":
                return PetsDetailSerializer
            case "create":
                return PetsCreateSerializer
            case "update" | "partial_update":
                return PetsUpdateSerializer
            case "destroy":
                return PetsDeleteSerializer

    def get_object(self) -> Pets:
        obj = super().get_object()
        obj.age = convert_birthday_to_age(obj.birthday)
        return obj


class ShelterUserRegistrationAPIView(CreateAPIView):
    serializer_class = ShelterUserRegistrationSerializer

    def perform_create(self, serializer: Type[T]) -> None:
        user = serializer.save()
        user.groups.add(Group.objects.get(name=READ_GROUP_NAME))
