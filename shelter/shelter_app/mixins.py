from django.db.models import QuerySet

from shelter_app.models import Pets


class ShelterQuerysetMixin:
    request = None
    model = Pets

    def get_queryset(self) -> QuerySet:
        if self.request.user.shelter is not None:
            return self.model.objects.filter(shelter=self.request.user.shelter)
        return self.model.objects.all()
