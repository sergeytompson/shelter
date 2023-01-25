from django.contrib.auth.models import Permission
from django.test import TestCase

from shelter_app.models import Shelters, Kinds, Pets, ShelterUser

from datetime import date


class SheltersModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Shelters.objects.create(name='тестовый приют')

    def test_name_params(self):
        shelter = Shelters.objects.get(name='тестовый приют')

        field_label = shelter._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Название приюта')

        max_length = shelter._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_photo_params(self):
        shelter = Shelters.objects.get(name='тестовый приют')

        field_label = shelter._meta.get_field('photo').verbose_name
        self.assertEqual(field_label, 'Фото')

        upload_to = shelter._meta.get_field('photo').upload_to
        self.assertEquals(upload_to, "photos/shelters/")

        blank = shelter._meta.get_field('photo').blank
        self.assertTrue(blank)

        null = shelter._meta.get_field('photo').null
        self.assertTrue(null)

    def test_str(self):
        shelter = Shelters.objects.get(name='тестовый приют')
        self.assertEqual(shelter.name, str(shelter))


class KindModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Kinds.objects.create(name='тестовый вид')

    def test_name_params(self):
        kind = Kinds.objects.get(name='тестовый вид')

        field_label = kind._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Вид животного')

        max_length = kind._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_str(self):
        kind = Kinds.objects.get(name='тестовый вид')
        self.assertEqual(kind.name, str(kind))


class PetModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_shelter = Shelters.objects.create(name='тестовый приют')
        test_kind = Kinds.objects.create(name='тестовый вид')
        Pets.objects.create(

            name='тестовое животное 1',
            birthday=date.today(),
            weight=1,
            height=2,
            shelter=test_shelter,
            kind=test_kind
        )

    def test_name_params(self):
        pet = Pets.objects.get(name='тестовое животное 1')

        field_label = pet._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Кличка')

        max_length = pet._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_birthday_params(self):
        pet = Pets.objects.get(name='тестовое животное 1')

        field_label = pet._meta.get_field('birthday').verbose_name
        self.assertEqual(field_label, 'Дата рождения')

    def test_arrival_date_params(self):
        pet = Pets.objects.get(name='тестовое животное 1')

        field_label = pet._meta.get_field('arrival_date').verbose_name
        self.assertEqual(field_label, 'Дата прибытия в приют')

        auto_now_add = pet._meta.get_field('arrival_date').auto_now_add
        self.assertTrue(auto_now_add)

    def test_weight_params(self):
        pet = Pets.objects.get(name='тестовое животное 1')

        field_label = pet._meta.get_field('weight').verbose_name
        self.assertEqual(field_label, 'Вес')

    def test_height_params(self):
        pet = Pets.objects.get(name='тестовое животное 1')

        field_label = pet._meta.get_field('height').verbose_name
        self.assertEqual(field_label, 'Рост')

    def test_signs_params(self):
        pet = Pets.objects.get(name='тестовое животное 1')

        field_label = pet._meta.get_field('signs').verbose_name
        self.assertEqual(field_label, 'Особые приметы')

        blank = pet._meta.get_field('signs').blank
        self.assertTrue(blank)

        null = pet._meta.get_field('signs').null
        self.assertTrue(null)

    def test_photo_params(self):
        pet = Pets.objects.get(name='тестовое животное 1')

        field_label = pet._meta.get_field('photo').verbose_name
        self.assertEqual(field_label, 'Фото')

        upload_to = pet._meta.get_field('photo').upload_to
        self.assertEquals(upload_to, "photos/pets/")

        blank = pet._meta.get_field('photo').blank
        self.assertTrue(blank)

        null = pet._meta.get_field('photo').null
        self.assertTrue(null)

    def test_deleted_params(self):
        pet = Pets.objects.get(name='тестовое животное 1')

        field_label = pet._meta.get_field('deleted').verbose_name
        self.assertEqual(field_label, 'Удаление')

        default = pet._meta.get_field('deleted').default
        self.assertFalse(default)

    def test_shelter_params(self):
        pet = Pets.objects.get(name='тестовое животное 1')

        field_label = pet._meta.get_field('shelter').verbose_name
        self.assertEqual(field_label, 'Прибывает в приюте')

    def test_kind_params(self):
        pet = Pets.objects.get(name='тестовое животное 1')

        field_label = pet._meta.get_field('kind').verbose_name
        self.assertEqual(field_label, 'Вид животного')

        blank = pet._meta.get_field('kind').blank
        self.assertTrue(blank)

        null = pet._meta.get_field('kind').null
        self.assertTrue(null)

    def test_soft_delete_manager(self):
        pet = Pets.objects.get(name='тестовое животное 1')
        pet.deleted = True
        pet.save()

        self.assertRaises(Pets.DoesNotExist, Pets.objects.get, name='тестовое животное 1')

    def test_restore(self):
        pet = Pets.all_objects.get(name='тестовое животное 1')
        pet.restore()
        pet.save()

        pet = Pets.objects.get(name='тестовое животное 1')
        self.assertFalse(pet.deleted)

    def test_delete(self):
        pet = Pets.objects.get(name='тестовое животное 1')
        pet.delete()
        pet.save()

        pet = Pets.all_objects.get(name='тестовое животное 1')
        self.assertTrue(pet.deleted)

    def test_str(self):
        pet = Pets.objects.get(name='тестовое животное 1')
        self.assertEqual(pet.name, str(pet))

    def test_get_absolute_url(self):
        pet = Pets.objects.get(name='тестовое животное 1')
        pk = pet.pk
        self.assertEquals(pet.get_absolute_url(), f'/pets/{pk}')


class ShelterUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_shelter = Shelters.objects.create(name='тестовый приют')
        ShelterUser.objects.create(username='тестовый юзер', shelter=test_shelter)

    def test_shelter_params(self):
        shelter_user = ShelterUser.objects.get(username='тестовый юзер')

        field_label = shelter_user._meta.get_field('shelter').verbose_name
        self.assertEqual(field_label, 'Привязан к приюту')
        # TODO наверное это лишнее
        blank = shelter_user._meta.get_field('shelter').blank
        self.assertTrue(blank)
        # TODO наверное это лишнее
        null = shelter_user._meta.get_field('shelter').null
        self.assertTrue(null)

    # TODO не уверен, нужно ли это
    def test_str(self):
        shelter_user = ShelterUser.objects.get(username='тестовый юзер')
        self.assertEqual(shelter_user.username, str(shelter_user))

    def test_has_add_pets_perm(self):
        shelter_user = ShelterUser.objects.get(username='тестовый юзер')
        self.assertFalse(shelter_user.has_add_pets_perm())

        shelter_user = ShelterUser.objects.get(username='тестовый юзер')
        perm = Permission.objects.get(name='Can add Животное')
        shelter_user.user_permissions.add(perm)
        self.assertTrue(shelter_user.has_add_pets_perm())

    def test_has_change_pets_perm(self):
        shelter_user = ShelterUser.objects.get(username='тестовый юзер')
        self.assertFalse(shelter_user.has_change_pets_perm())

        shelter_user = ShelterUser.objects.get(username='тестовый юзер')
        perm = Permission.objects.get(name='Can change Животное')
        shelter_user.user_permissions.add(perm)
        self.assertTrue(shelter_user.has_change_pets_perm())

    def test_has_delete_pets_perm(self):
        shelter_user = ShelterUser.objects.get(username='тестовый юзер')
        self.assertFalse(shelter_user.has_delete_pets_perm())

        shelter_user = ShelterUser.objects.get(username='тестовый юзер')
        perm = Permission.objects.get(name='Can delete Животное')
        shelter_user.user_permissions.add(perm)
        self.assertTrue(shelter_user.has_delete_pets_perm())

# TODO убирай хардкод по максимуму!

# TODO у моделей есть смысл тестировать самописные функции
#  и создание из валидных и невалидных данных, проверять является ли поле nullable или blankable
#  немного перебор, но и не ошибка
