from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse


class SoftDeleteManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(deleted=False)


class Shelters(models.Model):
    name = models.CharField("Название приюта", max_length=100)
    photo = models.ImageField(
        "Фото", upload_to="photos/shelters/", blank=True, null=True
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("shelter", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Приют"
        verbose_name_plural = "Приюты"


class Kinds(models.Model):
    name = models.CharField("Вид животного", max_length=100)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Вид животного"
        verbose_name_plural = "Виды животных"


class Pets(models.Model):
    name = models.CharField("Кличка", max_length=100)
    birthday = models.DateField("Дата рождения")
    arrival_date = models.DateField("Дата прибытия в приют", auto_now_add=True)
    weight = models.FloatField("Вес")
    height = models.FloatField("Рост")
    signs = models.TextField("Особые приметы", blank=True, null=True)
    photo = models.ImageField("Фото", upload_to="photos/pets/", blank=True, null=True)
    deleted = models.BooleanField("Удаление", default=False)
    shelter = models.ForeignKey(
        Shelters, on_delete=models.CASCADE, verbose_name="Прибывает в приюте"
    )
    kind = models.ForeignKey(
        Kinds,
        on_delete=models.SET_NULL,
        verbose_name="Вид животного",
        blank=True,
        null=True,
    )

    all_objects = models.Manager()
    objects = SoftDeleteManager()

    class Meta:
        verbose_name = "Животное"
        verbose_name_plural = "Животные"
        ordering = ("-arrival_date",)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("pet", kwargs={"pk": self.pk})

    def delete(self, using: Any = None, keep_parents: bool = False) -> None:
        self.deleted = True
        self.save()

    def restore(self) -> None:
        self.deleted = False
        self.save()


class ShelterUser(AbstractUser):
    shelter = models.ForeignKey(
        Shelters,
        on_delete=models.CASCADE,
        verbose_name="Привязан к приюту",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "пользователя приютов"
        verbose_name_plural = "Пользователи приютов"

    def __str__(self) -> str:
        return self.username

    def has_add_pets_perm(self) -> bool:
        return self.has_perm("shelter_app.add_pets")

    def has_change_pets_perm(self) -> bool:
        return self.has_perm("shelter_app.change_pets")

    def has_delete_pets_perm(self) -> bool:
        return self.has_perm("shelter_app.delete_pets")
