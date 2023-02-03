from datetime import date

from django.contrib.auth.models import Permission
from django.test import TestCase
from shelter_app.models import Kinds, Pets, Shelters, ShelterUser


class SheltersModelTest(TestCase):
    shelter_name = "тестовый приют"

    @classmethod
    def setUpTestData(cls):
        Shelters.objects.create(name=cls.shelter_name)

    def test_fields(self):
        shelter = Shelters.objects.get(name=self.shelter_name)
        test_data = {
            "name": (("verbose_name", "Название приюта"), ("max_length", 100)),
            "photo": (("verbose_name", "Фото"), ("upload_to", "photos/shelters/")),
        }

        for name_field, field_values in test_data.items():
            for field_param, expected_val in field_values:
                field_param_value = getattr(
                    shelter._meta.get_field(name_field), field_param
                )
                self.assertEqual(field_param_value, expected_val)

    def test_str(self):
        shelter = Shelters.objects.get(name=self.shelter_name)
        self.assertEqual(shelter.name, str(shelter))


class KindModelTest(TestCase):
    kind_name = "тестовый вид"

    @classmethod
    def setUpTestData(cls):
        Kinds.objects.create(name=cls.kind_name)

    def test_name_params(self):
        kind = Kinds.objects.get(name=self.kind_name)
        field_name = "name"

        field_label = kind._meta.get_field(field_name).verbose_name
        self.assertEqual(field_label, "Вид животного")

        max_length = kind._meta.get_field(field_name).max_length
        self.assertEquals(max_length, 100)

    def test_str(self):
        kind = Kinds.objects.get(name="тестовый вид")
        self.assertEqual(kind.name, str(kind))


class PetModelTest(TestCase):
    pet_name = "тестовое животное"

    @classmethod
    def setUpTestData(cls):
        test_shelter = Shelters.objects.create(name="тестовый приют")
        test_kind = Kinds.objects.create(name="тестовый вид")
        Pets.objects.create(
            name=cls.pet_name,
            birthday=date.today(),
            weight=1,
            height=2,
            shelter=test_shelter,
            kind=test_kind,
        )

    def test_fields(self):
        pet = Pets.objects.get(name=self.pet_name)
        test_data = {
            "name": (("verbose_name", "Кличка"), ("max_length", 100)),
            "birthday": (("verbose_name", "Дата рождения"),),
            "arrival_date": (
                ("verbose_name", "Дата прибытия в приют"),
                ("auto_now_add", True),
            ),
            "weight": (("verbose_name", "Вес"),),
            "height": (("verbose_name", "Рост"),),
            "signs": (("verbose_name", "Особые приметы"),),
            "photo": (("verbose_name", "Фото"), ("upload_to", "photos/pets/")),
            "deleted": (("verbose_name", "Удаление"), ("default", False)),
            "shelter": (("verbose_name", "Прибывает в приюте"),),
            "kind": (("verbose_name", "Вид животного"),),
        }

        for name_field, field_values in test_data.items():
            for field_param, expected_val in field_values:
                field_param_value = getattr(
                    pet._meta.get_field(name_field), field_param
                )
                self.assertEqual(field_param_value, expected_val)

    def test_soft_delete_manager(self):
        pet = Pets.objects.get(name=self.pet_name)
        pet.deleted = True
        pet.save()

        self.assertRaises(Pets.DoesNotExist, Pets.objects.get, name=self.pet_name)

    def test_restore(self):
        pet = Pets.all_objects.get(name=self.pet_name)
        pet.restore()
        pet.save()

        pet = Pets.objects.get(name=self.pet_name)
        self.assertFalse(pet.deleted)

    def test_delete(self):
        pet = Pets.objects.get(name=self.pet_name)
        pet.delete()
        pet.save()

        pet = Pets.all_objects.get(name=self.pet_name)
        self.assertTrue(pet.deleted)

    def test_str(self):
        pet = Pets.objects.get(name=self.pet_name)
        self.assertEqual(pet.name, str(pet))

    def test_get_absolute_url(self):
        pet = Pets.objects.get(name=self.pet_name)
        pk = pet.pk
        self.assertEquals(pet.get_absolute_url(), f"/pets/{pk}")


class ShelterUserModelTest(TestCase):
    username = "тестовый юзер"

    @classmethod
    def setUpTestData(cls):
        test_shelter = Shelters.objects.create(name="тестовый приют")
        ShelterUser.objects.create(username=cls.username, shelter=test_shelter)

    def test_shelter_params(self):
        shelter_user = ShelterUser.objects.get(username=self.username)

        field_label = shelter_user._meta.get_field("shelter").verbose_name
        self.assertEqual(field_label, "Привязан к приюту")

    def test_str(self):
        shelter_user = ShelterUser.objects.get(username=self.username)
        self.assertEqual(shelter_user.username, str(shelter_user))

    def test_has_add_pets_perm(self):
        shelter_user = ShelterUser.objects.get(username=self.username)
        self.assertFalse(shelter_user.has_add_pets_perm())

        shelter_user = ShelterUser.objects.get(username=self.username)
        perm = Permission.objects.get(name="Can add Животное")
        shelter_user.user_permissions.add(perm)
        self.assertTrue(shelter_user.has_add_pets_perm())

    def test_has_change_pets_perm(self):
        shelter_user = ShelterUser.objects.get(username=self.username)
        self.assertFalse(shelter_user.has_change_pets_perm())

        shelter_user = ShelterUser.objects.get(username=self.username)
        perm = Permission.objects.get(name="Can change Животное")
        shelter_user.user_permissions.add(perm)
        self.assertTrue(shelter_user.has_change_pets_perm())

    def test_has_delete_pets_perm(self):
        shelter_user = ShelterUser.objects.get(username=self.username)
        self.assertFalse(shelter_user.has_delete_pets_perm())

        shelter_user = ShelterUser.objects.get(username=self.username)
        perm = Permission.objects.get(name="Can delete Животное")
        shelter_user.user_permissions.add(perm)
        self.assertTrue(shelter_user.has_delete_pets_perm())
