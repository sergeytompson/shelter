from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Kinds, Pets, Shelters, ShelterUser


class ShelterUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(),
        error_messages={"required": ""},
    )
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput()
    )
    shelter = forms.ModelChoiceField(
        label="Приют",
        queryset=Shelters.objects.all(),
        empty_label="Выберете приют",
        widget=forms.Select(),
    )

    class Meta(UserCreationForm.Meta):
        model = ShelterUser
        fields = UserCreationForm.Meta.fields + ("shelter",)


class PetModelForm(forms.ModelForm):
    kind = forms.ModelChoiceField(
        label="Вид животного",
        queryset=Kinds.objects.all(),
        empty_label="Выберете вид животного",
        widget=forms.Select(),
    )

    class Meta:
        model = Pets
        fields = (
            "name",
            "kind",
            "birthday",
            "weight",
            "height",
            "signs",
            "photo",
        )
        widgets = {
            "birthday": forms.DateInput(),
            "weight": forms.NumberInput(),
            "height": forms.NumberInput(),
        }
