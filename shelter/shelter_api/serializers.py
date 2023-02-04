from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from shelter_app.models import Pets, ShelterUser


class PetsChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pets
        exclude = ("shelter", "deleted")


class PetsCreateSerializer(PetsChangeSerializer):
    pass


class PetsUpdateSerializer(PetsChangeSerializer):
    pass


class PetsDeleteSerializer(PetsChangeSerializer):
    pass


class PetsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pets
        fields = ("pk", "name")


class PetsDetailSerializer(serializers.ModelSerializer):
    kind = serializers.StringRelatedField()
    age = serializers.IntegerField()

    class Meta:
        model = Pets
        exclude = ("shelter", "deleted", "birthday")


class ShelterUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, label="Пароль", style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        label="Подтвердите пароль",
        write_only=True,
        validators=(validate_password,),
        style={"input_type": "password"},
    )

    class Meta:
        model = ShelterUser
        fields = ("username", "shelter", "password", "password2")

    def save(self, *args, **kwargs):
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({password: "Пароли не совпадают"})

        user = ShelterUser(
            username=self.validated_data["username"],
            shelter=self.validated_data["shelter"],
        )

        user.set_password(password)
        u = user.save()
        return user
