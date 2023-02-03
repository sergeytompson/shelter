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


# TODO еще есть rest_framework.generics - по структуре будет очень похоже на джанговские вьюхи

# TODO не нашел во вью проверку пермишенов и залогинен ли пользак

# TODO где аннотации?
class PetsViewSet(ShelterQuerysetMixin, ModelViewSet):
    # TODO list?
    permission_classes = [DjangoModelPermissions]

    def perform_create(self, serializer):
        if self.request.user.shelter is not None:
            serializer.save(shelter=self.request.user.shelter)
        else:
            raise ValidationError(
                "Пожалуйста, создайте новое животное в административной панели"
            )

    def get_serializer_class(self):
        # TODO в 3.10 появился pattern matching отличная возможность его попробовать
        #  https://peps.python.org/pep-0636/
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
        # TODO где то я этот кусок уже видел
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
        # TODO а может ли произойти ситуация, когда пользователь создался, а искомой группы нет?
        #  почитай про транзакции в бд и django orm  в частности
        user = serializer.save()
        # TODO старайся не использовать константы так, сделай константу в начале модуля или класса и подставляй уже ее
        user.groups.add(Group.objects.get(name="guest"))

    # TODO вот такой ответ дает api на мой запрос что же здесь не так?)
    """
    HTTP 201 Created
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept
    
    {
        "username": "username",
        "shelter": 2,
        "password": "000",
        "password2": "000"
    }
    """
