# Generated by Django 4.1.4 on 2022-12-20 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Вид животного')),
            ],
            options={
                'verbose_name': 'Вид животного',
                'verbose_name_plural': 'Виды животных',
            },
        ),
        migrations.CreateModel(
            name='Shelter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название приюта')),
                ('photo', models.ImageField(blank=True, upload_to='photos/shelters/', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Приют',
                'verbose_name_plural': 'Приюты',
            },
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Кличка')),
                ('birthday', models.DateTimeField(verbose_name='Дата рождения')),
                ('arrival_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата прибытия в приют')),
                ('weight', models.FloatField(verbose_name='Вес')),
                ('height', models.FloatField(verbose_name='Рост')),
                ('signs', models.TextField(blank=True, verbose_name='Особые приметы')),
                ('photo', models.ImageField(blank=True, upload_to='photos/pets/', verbose_name='Фото')),
                ('deleted_at', models.BooleanField(default=False, verbose_name='Удаление')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shelter_management.kind', verbose_name='Вид животного')),
                ('shelter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shelter_management.shelter', verbose_name='Прибывает в приюте')),
            ],
            options={
                'verbose_name': 'Животное',
                'verbose_name_plural': 'Животные',
                'ordering': ['-arrival_date'],
            },
        ),
    ]
