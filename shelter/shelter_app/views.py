from datetime import date
from typing import Union

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PetDeleteForm, PetModelForm, ShelterUserCreationForm
from .models import Pets, Shelters, ShelterUser


class PetsListView(LoginRequiredMixin, ListView):
    model = Pets
    context_object_name = "pets"
    login_url = "login"

    def get_queryset(self) -> QuerySet:
        if hasattr(self.request.user, "shelteruser"):
            return Pets.objects.filter(shelter=self.request.user.shelteruser.shelter)
        return Pets.objects.all()

# TODO не храним закомментированный код, это плохая привычка
# class ShelterListView(ListView):
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("It's Shelter List View")


# class ShelterDetailView(DetailView):
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("It's Shelter Detail View")


class PetDetailView(DetailView):
    model = Pets
    context_object_name = "pet"

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
    form_class = PetModelForm
    # TODO у create/update форма может быть и должна быть одной
    #  если провалишься внутрь класса createView - то увидишь, что класс будет искать
    #  хтмл шаблон {model_name}_form, всю логику по сохранение или апдейту Джанго возьмет на себя
    #  class CreateView(SingleObjectTemplateResponseMixin, BaseCreateView):
    #  template_name_suffix = "_form"
    template_name = "shelter_app/pet_create.html"
    raise_exception = True
    permission_required = "shelter_app.add_pets"


class PetUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = PetModelForm
    # TODO смотри комментарий выше
    template_name = "shelter_app/pet_update.html"
    raise_exception = True
    permission_required = "shelter_app.change_pets"

    def get_queryset(self) -> QuerySet:
        return Pets.objects.all()


class PetDeleteView(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    permission_required = "shelter_app.delete_pets"
    template_name = "shelter_app/pets_detail.html"
    form_class = PetDeleteForm

    def get_success_url(self) -> str:
        return reverse("pets")

    # TODO нет нужды в этом методе
    #  в переменных класс можно указать model = {твоя модель}
    #  логика по Model.objects.all() -> срабатывает по умолчанию
    #  если есть нужда в более специфичном кверисете, то
    #  можно указать переменную класса queryset = Model.objects.filter(что то там)
    #  функцию стоит использовать только тогда, когда есть какая то логика по получению квери сета
    def get_queryset(self) -> QuerySet:
        return Pets.objects.all()


class ShelterUserRegisterView(CreateView):
    form_class = ShelterUserCreationForm
    template_name = "shelter_app/register.html"
    success_url = reverse_lazy("login")

    def post(
        self, request: HttpRequest, *args, **kwargs
    ) -> Union[HttpResponseRedirect, HttpResponse]:
        form = self.get_form()
        if form.is_valid():
            new_user = form.save()
            new_user.groups.add(Group.objects.get(name="guest"))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ShelterUserLoginView(LoginView):
    template_name = "shelter_app/login.html"
