from django.http import HttpRequest

from .forms import PetDeleteForm


# TODO обычно контекст процессоры используют для глобальных объектов
#  например объект корзины в интернет магазине, глобально же хранить форму удаления
#  не самый логичный вариант
def get_context_data(request: HttpRequest) -> dict:
    context = {"pet_delete": PetDeleteForm()}
    return context
