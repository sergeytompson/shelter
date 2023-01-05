from django.conf.urls.static import static
from django.urls import path

from shelter import settings

from .views import *

urlpatterns = [
    path('', ShelterListView.as_view(), name='home'),
    path('shelters/<int:pk>', PetsListView.as_view(), name='shelter'),
    path('pets/<int:pk>', PetDetailView.as_view(), name='pet'),
    path('shelters/<int:pk>/create_pet', PetCreateView.as_view(), name='create pet'),
    path('pets/<int:pk>/update', PetUpdateView.as_view(), name='update pet'),
    path('pets/<int:pk>/delete', PetUpdateView.as_view(), name='delete pet'),
    path('register/', ShelterUserRegisterView.as_view(), name='register'),
    path('login/', ShelterUserLoginView.as_view(), name='login'),
    path('logout/', ShelterUserLogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
