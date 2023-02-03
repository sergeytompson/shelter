import datetime

from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from shelter_app.models import Kinds, Pets, Shelters, ShelterUser


class PetsListViewTest(TestCase):
    fixtures = ["shelter_fixtures.json"]
    username = "Гена"
    password = "парольгены"
    url = reverse("pets")

    @classmethod
    def setUpTestData(cls):
        cls.shelter = Shelters.objects.first()
        shelter_user = ShelterUser.objects.create_user(
            username=cls.username, password=cls.password, shelter=cls.shelter
        )
        shelter_user.groups.add(Group.objects.get(name="guest"))

    def test_redirect_unauthorized_user(self):
        resp = self.client.get(self.url)
        self.assertRedirects(resp, "/login/?next=/")

    def test_desired_status_to_authorized_user(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, "shelter_app/pets_list.html")

    def test_get_queryset(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url)
        self.assertEqual(
            len(resp.context["pets"]), len(Pets.objects.filter(shelter=self.shelter))
        )
        shelter = ShelterUser.objects.get(username=self.username).shelter
        self.assertQuerysetEqual(resp.context["pets"], shelter.pets_set.all())

        self.client.logout()
        superuser_name, superuser_password = "superuser", "superuserpassword"
        ShelterUser.objects.create_superuser(
            username=superuser_name, password=superuser_password
        )
        self.client.login(username=superuser_name, password=superuser_password)
        resp = self.client.get(self.url)
        self.assertEqual(len(resp.context["pets"]), len(Pets.objects.all()))

    def test_view_does_not_show_soft_delete_pets(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url)
        pet = resp.context["pets"][0]
        pet.delete()
        resp = self.client.get(self.url)
        self.assertTrue(pet not in resp.context["pets"])

    def test_view_show_links_to_users_with_relevant_perms(self):
        admin_user_name, admin_user_password = "Антон", "парольантона"
        admin_user = ShelterUser.objects.create_user(
            username=admin_user_name, password=admin_user_password, shelter=self.shelter
        )
        admin_user.groups.add(Group.objects.get(name="admin"))
        pets_count = len(Pets.objects.filter(shelter=admin_user.shelter))
        links_count = (pets_count, pets_count, 1)
        link_labels = ("Обновить", "Удалить", "Добавить животное")

        self.client.login(username=admin_user_name, password=admin_user_password)
        resp = self.client.get(self.url)
        for link_label, link_count in zip(link_labels, links_count):
            self.assertContains(resp, link_label, count=link_count)

        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url)
        for link_label in link_labels:
            self.assertNotContains(resp, link_label)


class PetDetailViewTest(TestCase):
    fixtures = ["shelter_fixtures.json"]
    username = "Гена"
    password = "парольгены"

    @classmethod
    def setUpTestData(cls):
        cls.shelter = Shelters.objects.first()
        cls.url_pet_from_user_shelter = reverse(
            "pet", kwargs={"pk": Pets.objects.filter(shelter=cls.shelter).first().pk}
        )
        cls.url_pet_from_other_shelter = reverse(
            "pet", kwargs={"pk": Pets.objects.exclude(shelter=cls.shelter).first().pk}
        )
        shelter_user = ShelterUser.objects.create_user(
            username=cls.username, password=cls.password, shelter=cls.shelter
        )
        shelter_user.groups.add(Group.objects.get(name="guest"))

    def test_redirect_unauthorized_user(self):
        resp = self.client.get(self.url_pet_from_user_shelter)
        self.assertRedirects(resp, f"/login/?next={self.url_pet_from_user_shelter}")

    def test_desired_status_to_authorized_user(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url_pet_from_user_shelter)
        self.assertEqual(resp.status_code, 200)

    def test_user_try_to_see_pet_not_from_his_shelter(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url_pet_from_other_shelter)
        self.assertEqual(resp.status_code, 404)

    def test_view_uses_correct_template(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url_pet_from_user_shelter)
        self.assertTemplateUsed(resp, "shelter_app/pets_detail.html")

    def test_view_does_not_show_soft_delete_pets(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url_pet_from_user_shelter)
        pet = resp.context["pet"]
        pet.delete()
        resp = self.client.get(self.url_pet_from_user_shelter)
        self.assertEqual(resp.status_code, 404)

    def test_view_show_links_to_users_with_relevant_perms(self):
        admin_user_name, admin_user_password = "Антон", "парольантона"
        admin_user = ShelterUser.objects.create_user(
            username=admin_user_name, password=admin_user_password, shelter=self.shelter
        )
        admin_user.groups.add(Group.objects.get(name="admin"))
        link_labels = ("Обновить", "Удалить", "Добавить животное")

        self.client.login(username=admin_user_name, password=admin_user_password)
        resp = self.client.get(self.url_pet_from_user_shelter)
        for link_label in link_labels:
            self.assertContains(resp, link_label, count=1)

        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url_pet_from_user_shelter)
        for link_label in link_labels:
            self.assertNotContains(resp, link_label)

    def test_get_context_data(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url_pet_from_user_shelter)
        pet_pk = resp.context["pet"].pk
        birthday = Pets.objects.get(pk=pet_pk).birthday
        today = datetime.date.today()
        self.assertEqual(
            today.year
            - birthday.year
            - ((today.month, today.day) < (birthday.month, birthday.day)),
            resp.context["age"],
        )


class PetCreateViewTest(TestCase):
    fixtures = ["shelter_fixtures.json"]
    username = "Виталик"
    password = "парольвиталика"
    url = reverse("pet create")

    @classmethod
    def setUpTestData(cls):
        cls.shelter = Shelters.objects.first()
        shelter_user = ShelterUser.objects.create_user(
            username=cls.username, password=cls.password, shelter=cls.shelter
        )
        shelter_user.groups.add(Group.objects.get(name="user"))

    def test_forbidden_unauthorized_user(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_forbidden_user_without_perm(self):
        guest_user_name, guest_user_password = "Гена", "парольгены"
        guest_user = ShelterUser.objects.create_user(
            username=guest_user_name, password=guest_user_password, shelter=self.shelter
        )
        guest_user.groups.add(Group.objects.get(name="guest"))
        self.client.login(username=guest_user_name, password=guest_user_password)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_desired_status_user_with_perm(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, "shelter_app/pets_form.html")

    def test_get_context_data(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url)
        self.assertEqual(resp.context["title"], "Создание животного")
        self.assertEqual(resp.context["button"], "Создать животное")

    def test_form_valid_invalid_name(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url, {"name": "a" * 101})
        self.assertFormError(
            resp,
            "form",
            "name",
            [
                "Убедитесь, что это значение содержит не более 100 символов (сейчас 101)."
            ],
        )
        resp = self.client.post(self.url, {"name": ""})
        self.assertFormError(resp, "form", "name", ["Обязательное поле."])
        resp = self.client.post(self.url, {"name": "Лапушка"})
        self.assertFormError(resp, "form", "name", [])

    def test_form_valid_invalid_kind(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url, {"kind": "чупокабра"})
        self.assertFormError(
            resp,
            "form",
            "kind",
            [
                "Выберите корректный вариант. Вашего варианта нет среди допустимых значений."
            ],
        )
        resp = self.client.post(self.url, {"kind": ""})
        self.assertFormError(resp, "form", "kind", ["Обязательное поле."])
        kind_pk = Kinds.objects.first().pk
        resp = self.client.post(self.url, {"kind": kind_pk})
        self.assertFormError(resp, "form", "kind", [])

    def test_form_valid_invalid_birthday(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url, {"birthday": "позавчера"})
        self.assertFormError(resp, "form", "birthday", ["Введите правильную дату."])
        resp = self.client.post(self.url, {"birthday": ""})
        self.assertFormError(resp, "form", "birthday", ["Обязательное поле."])
        resp = self.client.post(self.url, {"birthday": "11.08.2015"})
        self.assertFormError(resp, "form", "birthday", [])

    def test_form_valid_invalid_weight(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url, {"weight": "11 кило"})
        self.assertFormError(resp, "form", "weight", ["Введите число."])
        resp = self.client.post(self.url, {"weight": ""})
        self.assertFormError(resp, "form", "weight", ["Обязательное поле."])
        resp = self.client.post(self.url, {"weight": 13})
        self.assertFormError(resp, "form", "weight", [])

    def test_form_valid_invalid_height(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url, {"height": "метр с кепкой"})
        self.assertFormError(resp, "form", "height", ["Введите число."])
        resp = self.client.post(self.url, {"height": ""})
        self.assertFormError(resp, "form", "height", ["Обязательное поле."])
        resp = self.client.post(self.url, {"height": 13})
        self.assertFormError(resp, "form", "height", [])

    def test_form_valid_signs(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url, {"signs": ""})
        self.assertFormError(resp, "form", "signs", [])
        resp = self.client.post(reverse("pet create"), {"signs": "Просто Лапушка"})
        self.assertFormError(resp, "form", "signs", [])

    def test_form_valid_photo(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url, {"photo": "фото_лапушки"})
        self.assertFormError(resp, "form", "photo", [])
        resp = self.client.post(self.url, {"photo": ""})
        self.assertFormError(resp, "form", "photo", [])

    def test_redirect_valid_form(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(
            self.url,
            {
                "name": "Лапушка",
                "kind": 1,
                "birthday": "11.08.2015",
                "weight": 13,
                "height": 13,
                "signs": "Просто Лапушка",
                "photo": "фото_лапушки",
            },
        )
        pk = Pets.objects.get(name="Лапушка").pk
        self.assertRedirects(resp, f"/pets/{pk}")

    def test_invalid_form_for_superuser(self):
        superuser_name, superuser_password = "superuser", "superuserpassword"
        ShelterUser.objects.create_superuser(
            username=superuser_name, password=superuser_password
        )
        self.client.login(username=superuser_name, password=superuser_password)
        resp = self.client.post(
            self.url,
            {
                "name": "Лапушка",
                "kind": 1,
                "birthday": "11.08.2015",
                "weight": 13,
                "height": 13,
                "signs": "Просто Лапушка",
                "photo": "фото_лапушки",
            },
        )
        self.assertContains(
            resp, "Пожалуйста, создайте новое животное в административной панели"
        )


class PetUpdateViewTest(TestCase):
    fixtures = ["shelter_fixtures.json"]
    username = "Виталик"
    password = "парольвиталика"

    @classmethod
    def setUpTestData(cls):
        cls.shelter = Shelters.objects.first()
        cls.url_pet_from_user_shelter = reverse(
            "pet update",
            kwargs={"pk": Pets.objects.filter(shelter=cls.shelter).first().pk},
        )
        cls.url_pet_from_other_shelter = reverse(
            "pet update",
            kwargs={"pk": Pets.objects.exclude(shelter=cls.shelter).first().pk},
        )

        shelter_user = ShelterUser.objects.create_user(
            username=cls.username, password=cls.password, shelter=cls.shelter
        )
        shelter_user.groups.add(Group.objects.get(name="user"))

    def test_forbidden_unauthorized_user(self):
        resp = self.client.get(self.url_pet_from_user_shelter)
        self.assertEqual(resp.status_code, 403)

    def test_forbidden_user_without_perm(self):
        guest_user_name, guest_user_password = "Гена", "парольгены"
        guest_user = ShelterUser.objects.create_user(
            username=guest_user_name, password=guest_user_password, shelter=self.shelter
        )
        guest_user.groups.add(Group.objects.get(name="guest"))
        resp = self.client.get(self.url_pet_from_user_shelter)
        self.assertEqual(resp.status_code, 403)

    def test_404_for_user_from_another_shelter(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url_pet_from_other_shelter)
        self.assertEqual(resp.status_code, 404)

    def test_desired_status_user_with_perm(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url_pet_from_user_shelter)
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url_pet_from_user_shelter)
        self.assertTemplateUsed(resp, "shelter_app/pets_form.html")

    def test_get_context_data(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(self.url_pet_from_user_shelter)
        self.assertEqual(resp.context["title"], "Обновление информации о животном")
        self.assertEqual(resp.context["button"], "Обновить информацию")

    def test_form_valid_invalid_name(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url_pet_from_user_shelter, {"name": "a" * 101})
        self.assertFormError(
            resp,
            "form",
            "name",
            [
                "Убедитесь, что это значение содержит не более 100 символов (сейчас 101)."
            ],
        )
        resp = self.client.post(self.url_pet_from_user_shelter, {"name": ""})
        self.assertFormError(resp, "form", "name", ["Обязательное поле."])
        resp = self.client.post(self.url_pet_from_user_shelter, {"name": "Лапушка"})
        self.assertFormError(resp, "form", "name", [])

    def test_form_valid_invalid_kind(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url_pet_from_user_shelter, {"kind": "чупокабра"})
        self.assertFormError(
            resp,
            "form",
            "kind",
            [
                "Выберите корректный вариант. Вашего варианта нет среди допустимых значений."
            ],
        )
        resp = self.client.post(self.url_pet_from_user_shelter, {"kind": ""})
        self.assertFormError(resp, "form", "kind", ["Обязательное поле."])
        kind_pk = Kinds.objects.first().pk
        resp = self.client.post(self.url_pet_from_user_shelter, {"kind": kind_pk})
        self.assertFormError(resp, "form", "kind", [])

    def test_form_valid_invalid_birthday(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(
            self.url_pet_from_user_shelter, {"birthday": "позавчера"}
        )
        self.assertFormError(resp, "form", "birthday", ["Введите правильную дату."])
        resp = self.client.post(self.url_pet_from_user_shelter, {"birthday": ""})
        self.assertFormError(resp, "form", "birthday", ["Обязательное поле."])
        resp = self.client.post(
            self.url_pet_from_user_shelter, {"birthday": "11.08.2015"}
        )
        self.assertFormError(resp, "form", "birthday", [])

    def test_form_valid_invalid_weight(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url_pet_from_user_shelter, {"weight": "11 кило"})
        self.assertFormError(resp, "form", "weight", ["Введите число."])
        resp = self.client.post(self.url_pet_from_user_shelter, {"weight": ""})
        self.assertFormError(resp, "form", "weight", ["Обязательное поле."])
        resp = self.client.post(self.url_pet_from_user_shelter, {"weight": 13})
        self.assertFormError(resp, "form", "weight", [])

    def test_form_valid_invalid_height(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(
            self.url_pet_from_user_shelter, {"height": "метр с кепкой"}
        )
        self.assertFormError(resp, "form", "height", ["Введите число."])
        resp = self.client.post(self.url_pet_from_user_shelter, {"height": ""})
        self.assertFormError(resp, "form", "height", ["Обязательное поле."])
        resp = self.client.post(self.url_pet_from_user_shelter, {"height": 13})
        self.assertFormError(resp, "form", "height", [])

    def test_form_valid_signs(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url_pet_from_user_shelter, {"signs": ""})
        self.assertFormError(resp, "form", "signs", [])
        resp = self.client.post(
            self.url_pet_from_user_shelter, {"signs": "Просто Лапушка"}
        )
        self.assertFormError(resp, "form", "signs", [])

    def test_form_valid_photo(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(
            self.url_pet_from_user_shelter, {"photo": "фото_лапушки"}
        )
        self.assertFormError(resp, "form", "photo", [])
        resp = self.client.post(self.url_pet_from_user_shelter, {"photo": ""})
        self.assertFormError(resp, "form", "photo", [])

    def test_redirect_valid_form(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(
            self.url_pet_from_user_shelter,
            {
                "name": "Лапушка",
                "kind": 1,
                "birthday": "11.08.2015",
                "weight": 13,
                "height": 13,
                "signs": "Просто Лапушка",
                "photo": "фото_лапушки",
            },
        )
        redirect_url = self.url_pet_from_user_shelter.replace("/update", "")
        self.assertRedirects(resp, redirect_url)


class PetDeleteViewTest(TestCase):
    fixtures = ["shelter_fixtures.json"]
    username = "Антон"
    password = "парольантона"

    @classmethod
    def setUpTestData(cls):
        cls.shelter = Shelters.objects.first()
        cls.delete_pet_pk = Pets.objects.filter(shelter=cls.shelter).first().pk
        cls.url_pet_from_user_shelter = reverse(
            "pet delete", kwargs={"pk": cls.delete_pet_pk}
        )
        cls.url_pet_from_other_shelter = reverse(
            "pet delete",
            kwargs={"pk": Pets.objects.exclude(shelter=cls.shelter).first().pk},
        )
        shelter_user = ShelterUser.objects.create_user(
            username=cls.username, password=cls.password, shelter=cls.shelter
        )
        shelter_user.groups.add(Group.objects.get(name="admin"))

    def test_forbidden_unauthorized_user(self):
        resp = self.client.post(self.url_pet_from_user_shelter)
        self.assertEqual(resp.status_code, 403)
        self.assertFalse(Pets.all_objects.get(pk=self.delete_pet_pk).deleted)

    def test_forbidden_user_without_perm(self):
        guest_user_name, guest_user_password = "Гена", "парольгены"
        guest_user = ShelterUser.objects.create_user(
            username=guest_user_name, password=guest_user_password, shelter=self.shelter
        )
        guest_user.groups.add(Group.objects.get(name="guest"))
        self.client.login(username=guest_user_name, password=guest_user_password)
        resp = self.client.post(self.url_pet_from_user_shelter)
        self.assertEqual(resp.status_code, 403)
        self.assertFalse(Pets.all_objects.get(pk=self.delete_pet_pk).deleted)

    def test_404_for_user_from_another_shelter(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url_pet_from_other_shelter)
        self.assertEqual(resp.status_code, 404)
        self.assertFalse(Pets.all_objects.get(pk=self.delete_pet_pk).deleted)

    def test_success_for_user_with_perm(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(self.url_pet_from_user_shelter)
        self.assertRedirects(resp, "/")
        self.assertTrue(Pets.all_objects.get(pk=self.delete_pet_pk).deleted)


class ShelterUserRegisterViewTest(TestCase):
    fixtures = ["shelter_fixtures.json"]
    url = reverse("register")
    username = "Максим"
    password = "оченьсложныйпароль"

    @classmethod
    def setUpTestData(cls):
        cls.shelter_pk = Shelters.objects.first().pk

    def test_view_uses_correct_template(self):
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, "shelter_app/register.html")

    def test_form_valid_invalid_username(self):
        resp = self.client.post(self.url, {"username": "a" * 151})
        self.assertFormError(
            resp,
            "form",
            "username",
            [
                "Убедитесь, что это значение содержит не более 150 символов (сейчас 151)."
            ],
        )
        resp = self.client.post(self.url, {"username": ""})
        self.assertFormError(resp, "form", "username", [""])
        existing_user_name = ShelterUser.objects.first().username
        resp = self.client.post(self.url, {"username": existing_user_name})
        self.assertFormError(
            resp, "form", "username", ["Пользователь с таким именем уже существует."]
        )
        resp = self.client.post(self.url, {"username": self.username})
        self.assertFormError(resp, "form", "username", [])

    def test_form_valid_invalid_shelter(self):
        resp = self.client.post(self.url, {"shelter": "чупокабра"})
        self.assertFormError(
            resp,
            "form",
            "shelter",
            [
                "Выберите корректный вариант. Вашего варианта нет среди допустимых значений."
            ],
        )
        resp = self.client.post(self.url, {"shelter": ""})
        self.assertFormError(resp, "form", "shelter", ["Обязательное поле."])
        resp = self.client.post(self.url, {"shelter": self.shelter_pk})
        self.assertFormError(resp, "form", "shelter", [])

    def test_form_valid_invalid_password1(self):
        resp = self.client.post(self.url, {"password1": ""})
        self.assertFormError(resp, "form", "password1", ["Обязательное поле."])
        resp = self.client.post(self.url, {"password1": "@"})
        self.assertFormError(resp, "form", "password1", [])

    def test_form_valid_invalid_password2(self):
        resp = self.client.post(self.url, {"password2": ""})
        self.assertFormError(resp, "form", "password2", ["Обязательное поле."])
        resp = self.client.post(self.url, {"password2": "@"})
        self.assertFormError(
            resp,
            "form",
            "password2",
            [
                "Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов."
            ],
        )
        resp = self.client.post(self.url, {"password2": "12345678"})
        self.assertFormError(
            resp,
            "form",
            "password2",
            [
                "Введённый пароль слишком широко распространён.",
                "Введённый пароль состоит только из цифр.",
            ],
        )
        resp = self.client.post(self.url, {"password2": "abcdefgh"})
        self.assertFormError(
            resp,
            "form",
            "password2",
            ["Введённый пароль слишком широко распространён."],
        )
        resp = self.client.post(self.url, {"password2": self.password})
        self.assertFormError(resp, "form", "password2", [])

    def test_form_passwords_do_not_match(self):
        resp = self.client.post(
            self.url,
            {
                "username": self.username,
                "shelter": self.shelter_pk,
                "password1": "@",
                "password2": "$",
            },
        )
        self.assertFormError(
            resp, "form", "password2", ["Введенные пароли не совпадают."]
        )

    def test_form_success_redirect(self):
        resp = self.client.post(
            self.url,
            {
                "username": self.username,
                "shelter": self.shelter_pk,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertRedirects(resp, reverse("login"))
        self.assertTrue(ShelterUser.objects.filter(username=self.username).exists())
        self.assertEqual(
            ShelterUser.objects.get(username=self.username).shelter.pk, self.shelter_pk
        )


class ShelterUserLoginViewTest(TestCase):
    username = "Гена"
    password = "парольгены"
    url = reverse("login")

    @classmethod
    def setUpTestData(cls):
        cls.shelter = Shelters.objects.first()
        ShelterUser.objects.create_user(
            username=cls.username, password=cls.password, shelter=cls.shelter
        )

    def test_view_uses_correct_template(self):
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, "shelter_app/login.html")

    def test_form_invalid(self):
        resp = self.client.post(
            self.url,
            {
                "username": "",
                "password": "",
            },
        )
        self.assertFormError(resp, "form", "username", ["Обязательное поле."])
        self.assertFormError(resp, "form", "password", ["Обязательное поле."])

        resp = self.client.post(
            self.url,
            {
                "username": "гЕНА",
                "password": "ПАРОЛЬГЕНЫ",
            },
        )
        self.assertContains(
            resp,
            "Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.",
        )

        resp = self.client.post(
            self.url,
            {
                "username": self.username,
                "password": "парольвани",
            },
        )
        self.assertContains(
            resp,
            "Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.",
        )

        resp = self.client.post(
            self.url,
            {
                "username": "Максим",
                "password": "парольмаксима",
            },
        )
        self.assertContains(
            resp,
            "Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.",
        )

    def test_form_valid_redirect(self):
        resp = self.client.post(
            self.url,
            {
                "username": self.username,
                "password": self.password,
            },
        )
        self.assertRedirects(resp, reverse("pets"))
