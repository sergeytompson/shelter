# Generated by Django 4.1.4 on 2023-01-04 10:34

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Kinds",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="Вид животного"),
                ),
            ],
            options={
                "verbose_name": "Вид животного",
                "verbose_name_plural": "Виды животных",
            },
        ),
        migrations.CreateModel(
            name="Shelters",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="Название приюта"),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="photos/shelters/",
                        verbose_name="Фото",
                    ),
                ),
            ],
            options={
                "verbose_name": "Приют",
                "verbose_name_plural": "Приюты",
            },
        ),
        migrations.CreateModel(
            name="ShelterUser",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "shelter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shelter_app.shelters",
                        verbose_name="Привязан к приюту",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь приютов",
                "verbose_name_plural": "Пользователи приютов",
            },
            bases=("auth.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Pets",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Кличка")),
                ("birthday", models.DateField(verbose_name="Дата рождения")),
                (
                    "arrival_date",
                    models.DateField(
                        auto_now_add=True, verbose_name="Дата прибытия в приют"
                    ),
                ),
                ("weight", models.FloatField(verbose_name="Вес")),
                ("height", models.FloatField(verbose_name="Рост")),
                (
                    "signs",
                    models.TextField(
                        blank=True, null=True, verbose_name="Особые приметы"
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="photos/pets/",
                        verbose_name="Фото",
                    ),
                ),
                (
                    "deleted",
                    models.BooleanField(default=False, verbose_name="Удаление"),
                ),
                (
                    "kind",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="shelter_app.kinds",
                        verbose_name="Вид животного",
                    ),
                ),
                (
                    "shelter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shelter_app.shelters",
                        verbose_name="Прибывает в приюте",
                    ),
                ),
            ],
            options={
                "verbose_name": "Животное",
                "verbose_name_plural": "Животные",
                "ordering": ("-arrival_date",),
            },
        ),
    ]
