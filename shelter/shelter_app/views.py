from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.contrib.auth.views import LoginView, LogoutView

from .models import Pets, Shelters, ShelterUser


class PetsListView(LoginRequiredMixin, ListView):
    model = Pets
    context_object_name = 'pets'

    def get_queryset(self):
        # TODO немного странный подход, ты проверяешь является ли пользователь
        #  инстансом и потом подставляешь его аттрибут (который может быть None)
        #  не логичнее ли проверять наличие аттрибута и подставлять его, при наличии?
        if isinstance(self.request.user, ShelterUser):
            return Pets.objects.filter(shelter=self.request.user.shelter)
        return Pets.objects.all()

    def handle_no_permission(self):
        # TODO вместо текста лучше верни корректный http код
        return HttpResponse('пошел нахуй, пес')


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
