from datetime import date
from typing import Union

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.core.exceptions import EmptyResultSet, ValidationError
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ShelterUserCreationForm, PetModelForm
from .models import Pets


class PetsListView(LoginRequiredMixin, ListView):
    model = Pets
    context_object_name = "pets"
    login_url = "login"

    # TODO №1
    def get_queryset(self) -> QuerySet:
        if self.request.user.shelter is not None:
            return Pets.objects.filter(shelter=self.request.user.shelter)
        return Pets.objects.all()


class PetDetailView(LoginRequiredMixin, DetailView):
    model = Pets
    context_object_name = "pet"
    login_url = "login"

    # TODO №2
    def get_queryset(self):
        if self.request.user.shelter is not None:
            return self.model.objects.filter(shelter=self.request.user.shelter)
        return Pets.objects.all()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        pet = context["pet"]
        birthday = pet.birthday
        today = date.today()
        age = (
                today.year
                - birthday.year
                - ((today.month, today.day) < (birthday.month, birthday.day))
        )
        context["age"] = age
        return context


class PetCreateView(PermissionRequiredMixin, CreateView):
    model = Pets
    form_class = PetModelForm
    raise_exception = True
    permission_required = "shelter_app.add_pets"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание животного'
        context['button'] = 'Создать животное'
        return context

    # TODO переопределять целый метод post слишком жирно
    #  можно переопределение сделать более точечным
    #  внизу пример функции post у CreateView
    #  from: django/views/generic/edit.py
    """    
        def post(self, request, *args, **kwargs):
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
    """

    def post(
            self, request: HttpRequest, *args, **kwargs
    ) -> Union[HttpResponseRedirect, HttpResponse]:
        # TODO это скорее относится к контексту
        self.object = None
        form = self.get_form()
        if form.is_valid():
            pet = form.save(commit=False)
            if self.request.user.shelter is not None:
                pet.shelter = self.request.user.shelter
                return self.form_valid(form)
            else:
                messages.error(request, 'Пожалуйста, создайте новое животное в административной панели')
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


class PetUpdateView(PermissionRequiredMixin, UpdateView):
    model = Pets
    form_class = PetModelForm
    raise_exception = True
    permission_required = "shelter_app.change_pets"
    # TODO у тебя есть метод get_queryset, зачем тебе еще атрибут класса?
    queryset = Pets.objects.all()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновление информации о животном'
        context['button'] = 'Обновить информацию'
        return context

    # TODO №3
    def get_queryset(self):
        if self.request.user.shelter is not None:
            return self.model.objects.filter(shelter=self.request.user.shelter)
        return Pets.objects.all()


class PetDeleteView(PermissionRequiredMixin, DeleteView):
    model = Pets
    raise_exception = True
    permission_required = "shelter_app.delete_pets"

    def get_success_url(self) -> str:
        return reverse("pets")

    # TODO №4
    def get_queryset(self):
        if self.request.user.shelter is not None:
            return self.model.objects.filter(shelter=self.request.user.shelter)
        return Pets.objects.all()


class ShelterUserRegisterView(CreateView):
    form_class = ShelterUserCreationForm
    template_name = "shelter_app/register.html"
    success_url = reverse_lazy("login")

    # TODO как и в комменте ранее, можно значительно упростить
    def post(
            self, request: HttpRequest, *args, **kwargs
    ) -> Union[HttpResponseRedirect, HttpResponse]:
        self.object = None
        form = self.get_form()
        if form.is_valid():
            new_user = form.save()
            new_user.groups.add(Group.objects.get(name="guest"))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ShelterUserLoginView(LoginView):
    template_name = "shelter_app/login.html"

# TODO у тебя один и тот же метод явно определен 4!!! раза в одном модуле - явно требуется оптимизация
