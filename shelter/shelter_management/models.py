from django.db import models
from django.urls import reverse


class Shelter(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название приюта')
    photo = models.ImageField(upload_to='photos/shelters/', verbose_name='Фото', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('news', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Приют'
        verbose_name_plural = 'Приюты'


class Kind(models.Model):
    name = models.CharField(max_length=100, verbose_name='Вид животного')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид животного'
        verbose_name_plural = 'Виды животных'


class Pet(models.Model):
    name = models.CharField(max_length=100, verbose_name='Кличка')
    birthday = models.DateTimeField(verbose_name='Дата рождения')
    arrival_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата прибытия в приют')
    weight = models.FloatField(verbose_name='Вес')
    height = models.FloatField(verbose_name='Рост')
    signs = models.TextField(blank=True, verbose_name='Особые приметы')
    photo = models.ImageField(upload_to='photos/pets/', verbose_name='Фото', blank=True)
    deleted_at = models.BooleanField(default=False, verbose_name='Удаление')
    shelter = models.ForeignKey(Shelter, on_delete=models.PROTECT, verbose_name='Прибывает в приюте')
    kind = models.ForeignKey(Kind, on_delete=models.PROTECT, verbose_name='Вид животного')

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'
        ordering = ['-arrival_date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('news', kwargs={'pk': self.pk})
