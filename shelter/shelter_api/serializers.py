from rest_framework import serializers

from shelter_app.models import Pets, ShelterUser


# TODO такой нэйминг никуда не годится
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
        # TODO почему используется list?
        fields = ["username", "shelter", "password", "password2"]

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
