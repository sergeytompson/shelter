from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Shelters(models.Model):
    name = models.CharField("Название приюта", max_length=100)
    photo = models.ImageField(
        "Фото", upload_to="photos/shelters/", blank=True, null=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shelter", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Приют"
        verbose_name_plural = "Приюты"


class Kinds(models.Model):
    name = models.CharField("Вид животного", max_length=100)

    def __str__(self):
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

    class Meta:
        verbose_name = "Животное"
        verbose_name_plural = "Животные"
        ordering = ["-arrival_date"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("pet", kwargs={"pk": self.pk})

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def restore(self):
        self.deleted = False
        self.save()


class ShelterUser(User):

    shelter = models.ForeignKey(
        Shelters, on_delete=models.CASCADE, verbose_name="Привязан к приюту"
    )

    class Meta:
        verbose_name = "Пользователь приютов"
        verbose_name_plural = "Пользователи приютов"
