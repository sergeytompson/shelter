from django import forms
from django.test import TestCase

from shelter_app.forms import ShelterUserCreationForm, PetModelForm


# TODO ну это немного лишнее, под "тестом формы" имелось ввиду тестирование вью, где эта форма используется
class ShelterUserCreationFormTest(TestCase):

    def test_username_params(self):
        form = ShelterUserCreationForm()
        self.assertEqual(form.fields['username'].label, "Имя пользователя")
        self.assertIsInstance(form.fields['username'].widget, forms.TextInput)
        self.assertEqual(form.fields['username'].error_messages, {"required": ""})

    def test_password1_params(self):
        form = ShelterUserCreationForm()
        self.assertEqual(form.fields['password1'].label, "Пароль")
        self.assertIsInstance(form.fields['password1'].widget, forms.PasswordInput)

    def test_password2_params(self):
        form = ShelterUserCreationForm()
        self.assertEqual(form.fields['password2'].label, "Подтверждение пароля")
        self.assertIsInstance(form.fields['password1'].widget, forms.PasswordInput)

    def test_shelter_params(self):
        form = ShelterUserCreationForm()
        self.assertEqual(form.fields['shelter'].label, "Приют")
        self.assertEqual(form.fields['shelter'].empty_label, "Выберете приют")
        self.assertIsInstance(form.fields['shelter'].widget, forms.Select)


class PetModelFormTest(TestCase):

    def test_kind_params(self):
        form = PetModelForm()
        self.assertEqual(form.fields['kind'].label, "Вид животного")
        self.assertEqual(form.fields['kind'].empty_label, "Выберете вид животного")
        self.assertIsInstance(form.fields['kind'].widget, forms.Select)
