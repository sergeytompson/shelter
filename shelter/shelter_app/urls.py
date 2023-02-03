from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from shelter import settings

from .views import *

urlpatterns = [
    path("pets/<int:pk>", PetDetailView.as_view(), name="pet"),
    path("", PetsListView.as_view(), name="pets"),
    path("pet_create", PetCreateView.as_view(), name="pet create"),
    path("pets/<int:pk>/update", PetUpdateView.as_view(), name="pet update"),
    path("pets/<int:pk>/delete", PetDeleteView.as_view(), name="pet delete"),
    path("register/", ShelterUserRegisterView.as_view(), name="register"),
    path("login/", ShelterUserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
