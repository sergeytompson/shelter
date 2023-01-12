from django.http import HttpRequest

from .forms import PetDeleteForm


def get_context_data(request: HttpRequest) -> dict:
    context = {"pet_delete": PetDeleteForm()}
    return context
