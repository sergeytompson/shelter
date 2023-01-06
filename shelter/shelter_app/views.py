from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import DeletionMixin

from .models import Pets, Shelters, ShelterUser


class PetsListView(DeletionMixin, ListView):

    def get(self, request, *args, **kwargs):
        return HttpResponse("It's Pets List View")


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
        return HttpResponse("It's Create Pet View")


# class PetUpdateView(UpdateView):
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("It's Update Pet View")


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
