from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Pets, Shelters, ShelterUser

# from django.contrib.auth.views import LoginView, LogoutView




class PetsListView(LoginRequiredMixin, ListView):
    model = Pets
    context_object_name = "pets"
    raise_exception = True

    def get_queryset(self) -> QuerySet:
        if hasattr(self.request.user, "shelter"):
            return Pets.objects.filter(shelter=self.request.user.shelter)
        return Pets.objects.all()


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


class PetCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("It's Pet Create View")


# class PetUpdateView(UpdateView):
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("It's Pet Update View")


# class PetDeleteView(DeleteView):
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("It's Delete Pet View")


# class ShelterUserRegisterView(CreateView):
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("It's Shelter User Register View")


# class ShelterUserLoginView(LoginView):
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("It's Shelter User Login View")


# class ShelterUserLogoutView(LogoutView):
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("It's Shelter User Logout View")
