from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import DeletionMixin

from .models import Pets, Shelters, ShelterUser


class PetsListView(ListView):
    model = Pets
    context_object_name = 'pets'

    # TODO почитай про LoginRequiredMixin
    #  тебе незачем переопределять get метод, достаточно переопределить метод для получения queryset
    def get(self, request, *args, **kwargs):
        user = request.user

        if isinstance(user, ShelterUser):
            self.queryset = Pets.objects.filter(shelter=user.shelter)
        elif isinstance(request.user, AnonymousUser):
            return HttpResponse('Пошел нахуй, пес')
        return super().get(self, request, *args, **kwargs)


# class ShelterListView(ListView):
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("It's Shelter List View")


# class ShelterDetailView(DetailView):
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("It's Shelter Detail View")


# class PetDetailView(DetailView):
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("It's Pet Detail View")


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
