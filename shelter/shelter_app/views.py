from datetime import date
from typing import Union

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PetModelForm, ShelterUserCreationForm
from .models import Pets


class ShelterQuerysetMixin:
    request = None

    def get_queryset(self) -> QuerySet:
        if self.request.user.shelter is not None:
            return Pets.objects.filter(shelter=self.request.user.shelter)
        return Pets.objects.all()


class PetsListView(LoginRequiredMixin, ShelterQuerysetMixin, ListView):
    model = Pets
    context_object_name = "pets"
    login_url = "login"


class PetDetailView(LoginRequiredMixin, ShelterQuerysetMixin, DetailView):
    model = Pets
    context_object_name = "pet"
    login_url = "login"

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
        context["title"] = "Создание животного"
        context["button"] = "Создать животное"
        return context

    def form_valid(self, form):
        if self.request.user.shelter is not None:
            pet = form.save(commit=False)
            pet.shelter = self.request.user.shelter
            return super().form_valid(form)
        else:
            messages.error(
                self.request,
                "Пожалуйста, создайте новое животное в административной панели",
            )
            return self.form_invalid(form)


class PetUpdateView(PermissionRequiredMixin, ShelterQuerysetMixin, UpdateView):
    model = Pets
    form_class = PetModelForm
    raise_exception = True
    permission_required = "shelter_app.change_pets"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["title"] = "Обновление информации о животном"
        context["button"] = "Обновить информацию"
        return context


class PetDeleteView(PermissionRequiredMixin, ShelterQuerysetMixin, DeleteView):
    model = Pets
    raise_exception = True
    permission_required = "shelter_app.delete_pets"

    def get_success_url(self) -> str:
        return reverse("pets")


class ShelterUserRegisterView(CreateView):
    form_class = ShelterUserCreationForm
    template_name = "shelter_app/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        self.object = form.save()
        self.object.groups.add(Group.objects.get(name="guest"))
        return HttpResponseRedirect(self.get_success_url())


class ShelterUserLoginView(LoginView):
    template_name = "shelter_app/login.html"
