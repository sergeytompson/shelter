from rest_framework import serializers

from shelter_app.models import Pets, ShelterUser


class PetsCrtUpdDelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pets
        exclude = ("shelter", "deleted")


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
    password2 = serializers.CharField()

    class Meta:
        model = ShelterUser
        fields = ["username", "shelter", "password", "password2"]

    def save(self, *args, **kwargs):
        user = ShelterUser(
            username=self.validated_data["username"],
            shelter=self.validated_data["shelter"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({password: "Пароли не совпадают"})
        user.set_password(password)
        user.save()
        return user
