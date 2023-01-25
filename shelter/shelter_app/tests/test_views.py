import datetime

from django.test import TestCase
from django.urls import reverse

from shelter_app.models import ShelterUser, Pets


class PetsListViewTest(TestCase):
    fixtures = ['shelter_fixtures.json']

    def test_redirect_unauthorized_user(self):
        resp = self.client.get(reverse('pets'))
        self.assertRedirects(resp, '/login/?next=/')

    def test_desired_status_to_authorized_user(self):
        # TODO убирай хардкод, если у Валеры изменится пароль, мы же с ума сойдем менять его в каждом месте
        self.client.login(username='Валера', password='парольвалеры')
        resp = self.client.get(reverse('pets'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='Валера', password='парольвалеры')
        resp = self.client.get(reverse('pets'))
        self.assertTemplateUsed(resp, 'shelter_app/pets_list.html')

    def test_get_queryset(self):
        self.client.login(username='Валера', password='парольвалеры')
        resp = self.client.get(reverse('pets'))
        # TODO что такое "5"?
        self.assertEqual(len(resp.context['pets']), 5)
        shelter = ShelterUser.objects.get(username='Валера').shelter
        self.assertQuerysetEqual(resp.context['pets'], shelter.pets_set.all())

        self.client.logout()
        ShelterUser.objects.create_superuser('superuser', password='superuserpassword')
        self.client.login(username='superuser', password='superuserpassword')
        resp = self.client.get(reverse('pets'))
        # TODO что такое "25"?
        self.assertEqual(len(resp.context['pets']), 25)

        # TODO то есть если фикстура вдруг изменится, придется переписывать тесты?

    def test_view_does_not_show_soft_delete_pets(self):
        self.client.login(username='Валера', password='парольвалеры')
        resp = self.client.get(reverse('pets'))
        pet = resp.context['pets'][0]
        pet.delete()
        resp = self.client.get(reverse('pets'))
        self.assertTrue(pet not in resp.context['pets'])

    def test_view_show_links_to_users_with_relevant_perms(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.get(reverse('pets'))
        self.assertContains(resp, 'Обновить', count=5)
        self.assertContains(resp, 'Удалить', count=5)
        self.assertContains(resp, 'Добавить животное', count=1)

        self.client.login(username='Валера', password='парольвалеры')
        resp = self.client.get(reverse('pets'))
        self.assertNotContains(resp, 'Обновить')
        self.assertNotContains(resp, 'Удалить')
        self.assertNotContains(resp, 'Добавить животное')


class PetDetailViewTest(TestCase):
    fixtures = ['shelter_fixtures.json']

    def test_redirect_unauthorized_user(self):
        url = '/pets/1'
        resp = self.client.get(url)
        self.assertRedirects(resp, f'/login/?next={url}')

    def test_desired_status_to_authorized_user(self):
        self.client.login(username='Валера', password='парольвалеры')
        url = '/pets/20'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_user_try_to_see_pet_not_from_his_shelter(self):
        self.client.login(username='Валера', password='парольвалеры')
        url = '/pets/1'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_view_uses_correct_template(self):
        self.client.login(username='Валера', password='парольвалеры')
        resp = self.client.get('/pets/20')
        self.assertTemplateUsed(resp, 'shelter_app/pets_detail.html')

    def test_view_does_not_show_soft_delete_pets(self):
        self.client.login(username='Валера', password='парольвалеры')
        resp = self.client.get('/pets/20')
        pongo = resp.context['pet']
        pongo.delete()
        resp = self.client.get('/pets/20')
        self.assertEqual(resp.status_code, 404)

    def test_view_show_links_to_users_with_relevant_perms(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.get('/pets/20')
        self.assertContains(resp, 'Обновить', count=1)
        self.assertContains(resp, 'Удалить', count=1)
        self.assertContains(resp, 'Добавить животное', count=1)

        self.client.login(username='Валера', password='парольвалеры')
        resp = self.client.get('/pets/20')
        self.assertNotContains(resp, 'Обновить')
        self.assertNotContains(resp, 'Удалить')
        self.assertNotContains(resp, 'Добавить животное')

    def test_get_context_data(self):
        self.client.login(username='Валера', password='парольвалеры')
        resp = self.client.get('/pets/20')
        birthday = Pets.objects.get(pk=20).birthday
        today = datetime.date.today()
        self.assertEqual(
            today.year
            - birthday.year
            - ((today.month, today.day) < (birthday.month, birthday.day)),
            resp.context['age']
        )


class PetCreateViewTest(TestCase):
    fixtures = ['shelter_fixtures.json']

    def test_forbidden_unauthorized_user(self):
        resp = self.client.get(reverse('pet create'))
        self.assertEqual(resp.status_code, 403)

    def test_forbidden_user_without_perm(self):
        self.client.login(username='Валера', password='парольвалеры')
        resp = self.client.get(reverse('pet create'))
        self.assertEqual(resp.status_code, 403)

    def test_desired_status_user_with_perm(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.get(reverse('pet create'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.get(reverse('pet create'))
        self.assertTemplateUsed(resp, 'shelter_app/pets_form.html')

    def test_get_context_data(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.get(reverse('pet create'))
        self.assertEqual(resp.context['title'], 'Создание животного')
        self.assertEqual(resp.context['button'], 'Создать животное')

    def test_form_valid_invalid_name(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet create'), {'name': 'a' * 101})
        self.assertFormError(resp, 'form', 'name',
                             ['Убедитесь, что это значение содержит не более 100 символов (сейчас 101).'])
        resp = self.client.post(reverse('pet create'), {'name': ''})
        self.assertFormError(resp, 'form', 'name', ['Обязательное поле.'])
        resp = self.client.post(reverse('pet create'), {'name': 'Лапушка'})
        self.assertFormError(resp, 'form', 'name', [])

    def test_form_valid_invalid_kind(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet create'), {'kind': 'чупокабра'})
        self.assertFormError(resp, 'form', 'kind',
                             ['Выберите корректный вариант. Вашего варианта нет среди допустимых значений.'])
        resp = self.client.post(reverse('pet create'), {'kind': ''})
        self.assertFormError(resp, 'form', 'kind', ['Обязательное поле.'])
        resp = self.client.post(reverse('pet create'), {'kind': 1})
        self.assertFormError(resp, 'form', 'kind', [])

    def test_form_valid_invalid_birthday(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet create'), {'birthday': 'позавчера'})
        self.assertFormError(resp, 'form', 'birthday',
                             ['Введите правильную дату.'])
        resp = self.client.post(reverse('pet create'), {'birthday': ''})
        self.assertFormError(resp, 'form', 'birthday', ['Обязательное поле.'])
        resp = self.client.post(reverse('pet create'), {'birthday': '11.08.2015'})
        self.assertFormError(resp, 'form', 'birthday', [])

    def test_form_valid_invalid_weight(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet create'), {'weight': 'позавчера'})
        self.assertFormError(resp, 'form', 'weight', ['Введите число.'])
        resp = self.client.post(reverse('pet create'), {'weight': ''})
        self.assertFormError(resp, 'form', 'weight', ['Обязательное поле.'])
        resp = self.client.post(reverse('pet create'), {'weight': 13})
        self.assertFormError(resp, 'form', 'weight', [])

    def test_form_valid_invalid_height(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet create'), {'height': 'позавчера'})
        self.assertFormError(resp, 'form', 'height', ['Введите число.'])
        resp = self.client.post(reverse('pet create'), {'height': ''})
        self.assertFormError(resp, 'form', 'height', ['Обязательное поле.'])
        resp = self.client.post(reverse('pet create'), {'height': 13})
        self.assertFormError(resp, 'form', 'height', [])

    def test_form_valid_signs(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet create'), {'signs': ''})
        self.assertFormError(resp, 'form', 'signs', [])
        resp = self.client.post(reverse('pet create'), {'signs': 'Просто Лапушка'})
        self.assertFormError(resp, 'form', 'signs', [])

    def test_form_valid_photo(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet create'), {'photo': 'фото_лапушки'})
        self.assertFormError(resp, 'form', 'photo', [])
        resp = self.client.post(reverse('pet create'), {'photo': ''})
        self.assertFormError(resp, 'form', 'photo', [])

    def test_redirect_valid_form(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet create'), {
            'name': 'Лапушка',
            'kind': 1,
            'birthday': '11.08.2015',
            'weight': 13,
            'height': 13,
            'signs': 'Просто Лапушка',
            'photo': 'фото_лапушки'
        })
        pk = Pets.objects.get(name='Лапушка').pk
        self.assertRedirects(resp, f'/pets/{pk}')

    def test_invalid_form_for_superuser(self):
        ShelterUser.objects.create_superuser('superuser', password='superuserpassword')
        self.client.login(username='superuser', password='superuserpassword')
        resp = self.client.post(reverse('pet create'), {
            'name': 'Лапушка',
            'kind': 1,
            'birthday': '11.08.2015',
            'weight': 13,
            'height': 13,
            'signs': 'Просто Лапушка',
            'photo': 'фото_лапушки'
        })
        self.assertContains(resp, 'Пожалуйста, создайте новое животное в административной панели')


class PetUpdateViewTest(TestCase):
    fixtures = ['shelter_fixtures.json']

    def test_forbidden_unauthorized_user(self):
        resp = self.client.get('/pets/20/update')
        self.assertEqual(resp.status_code, 403)

    def test_forbidden_user_without_perm(self):
        self.client.login(username='Валера', password='парольвалеры')
        resp = self.client.get('/pets/20/update')
        self.assertEqual(resp.status_code, 403)

    def test_404_for_user_from_another_shelter(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.get('/pets/13/update')
        self.assertEqual(resp.status_code, 404)

    def test_desired_status_user_with_perm(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.get('/pets/20/update')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.get('/pets/20/update')
        self.assertTemplateUsed(resp, 'shelter_app/pets_form.html')

    def test_get_context_data(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.get('/pets/20/update')
        self.assertEqual(resp.context['title'], 'Обновление информации о животном')
        self.assertEqual(resp.context['button'], 'Обновить информацию')

    def test_form_valid_invalid_name(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'name': 'a' * 101})
        self.assertFormError(resp, 'form', 'name',
                             ['Убедитесь, что это значение содержит не более 100 символов (сейчас 101).'])
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'name': ''})
        self.assertFormError(resp, 'form', 'name', ['Обязательное поле.'])
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'name': 'Лапушка'})
        self.assertFormError(resp, 'form', 'name', [])

    def test_form_valid_invalid_kind(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'kind': 'чупокабра'})
        self.assertFormError(resp, 'form', 'kind',
                             ['Выберите корректный вариант. Вашего варианта нет среди допустимых значений.'])
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'kind': ''})
        self.assertFormError(resp, 'form', 'kind', ['Обязательное поле.'])
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'kind': 1})
        self.assertFormError(resp, 'form', 'kind', [])

    def test_form_valid_invalid_birthday(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'birthday': 'позавчера'})
        self.assertFormError(resp, 'form', 'birthday',
                             ['Введите правильную дату.'])
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'birthday': ''})
        self.assertFormError(resp, 'form', 'birthday', ['Обязательное поле.'])
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'birthday': '11.08.2015'})
        self.assertFormError(resp, 'form', 'birthday', [])

    def test_form_valid_invalid_weight(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'weight': 'позавчера'})
        self.assertFormError(resp, 'form', 'weight', ['Введите число.'])
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'weight': ''})
        self.assertFormError(resp, 'form', 'weight', ['Обязательное поле.'])
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'weight': 13})
        self.assertFormError(resp, 'form', 'weight', [])

    def test_form_valid_invalid_height(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'height': 'позавчера'})
        self.assertFormError(resp, 'form', 'height', ['Введите число.'])
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'height': ''})
        self.assertFormError(resp, 'form', 'height', ['Обязательное поле.'])
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'height': 13})
        self.assertFormError(resp, 'form', 'height', [])

    def test_form_valid_signs(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'signs': ''})
        self.assertFormError(resp, 'form', 'signs', [])
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'signs': 'Просто Лапушка'})
        self.assertFormError(resp, 'form', 'signs', [])

    def test_form_valid_photo(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'photo': 'фото_лапушки'})
        self.assertFormError(resp, 'form', 'photo', [])
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {'photo': ''})
        self.assertFormError(resp, 'form', 'photo', [])

    def test_redirect_valid_form(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet update', kwargs={'pk': 20}), {
            'name': 'Лапушка',
            'kind': 1,
            'birthday': '11.08.2015',
            'weight': 13,
            'height': 13,
            'signs': 'Просто Лапушка',
            'photo': 'фото_лапушки'
        })
        self.assertRedirects(resp, '/pets/20')


class PetDeleteViewTest(TestCase):
    fixtures = ['shelter_fixtures.json']

    def test_forbidden_unauthorized_user(self):
        resp = self.client.post(reverse('pet delete', kwargs={'pk': 20}))
        self.assertEqual(resp.status_code, 403)
        self.assertFalse(Pets.all_objects.get(pk=20).deleted)

    def test_forbidden_user_without_perm(self):
        self.client.login(username='Валера', password='парольвалеры')
        resp = self.client.post(reverse('pet delete', kwargs={'pk': 20}))
        self.assertEqual(resp.status_code, 403)
        self.assertFalse(Pets.all_objects.get(pk=20).deleted)

    def test_404_for_user_from_another_shelter(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet delete', kwargs={'pk': 13}))
        self.assertEqual(resp.status_code, 404)
        self.assertFalse(Pets.all_objects.get(pk=20).deleted)

    def test_success_for_user_with_perm(self):
        self.client.login(username='Ваня', password='парольвани')
        resp = self.client.post(reverse('pet delete', kwargs={'pk': 20}))
        self.assertRedirects(resp, '/')
        self.assertTrue(Pets.all_objects.get(pk=20).deleted)


class ShelterUserRegisterViewTest(TestCase):
    fixtures = ['shelter_fixtures.json']

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('register'))
        self.assertTemplateUsed(resp, 'shelter_app/register.html')

    def test_form_valid_invalid_username(self):
        resp = self.client.post(reverse('register'), {'username': 'a' * 151})
        self.assertFormError(resp, 'form', 'username',
                             ['Убедитесь, что это значение содержит не более 150 символов (сейчас 151).'])
        resp = self.client.post(reverse('register'), {'username': ''})
        self.assertFormError(resp, 'form', 'username', [''])
        resp = self.client.post(reverse('register'), {'username': 'Ваня'})
        self.assertFormError(resp, 'form', 'username', ['Пользователь с таким именем уже существует.'])
        resp = self.client.post(reverse('register'), {'username': 'Максим'})
        self.assertFormError(resp, 'form', 'username', [])

    def test_form_valid_invalid_shelter(self):
        resp = self.client.post(reverse('register'), {'shelter': 'чупокабра'})
        self.assertFormError(resp, 'form', 'shelter',
                             ['Выберите корректный вариант. Вашего варианта нет среди допустимых значений.'])
        resp = self.client.post(reverse('register'), {'shelter': ''})
        self.assertFormError(resp, 'form', 'shelter', ['Обязательное поле.'])
        resp = self.client.post(reverse('register'), {'shelter': 2})
        self.assertFormError(resp, 'form', 'shelter', [])

    def test_form_valid_invalid_password1(self):
        resp = self.client.post(reverse('register'), {'password1': ''})
        self.assertFormError(resp, 'form', 'password1', ['Обязательное поле.'])
        resp = self.client.post(reverse('register'), {'password1': '@'})
        self.assertFormError(resp, 'form', 'password1', [])

    def test_form_valid_invalid_password2(self):
        resp = self.client.post(reverse('register'), {'password2': ''})
        self.assertFormError(resp, 'form', 'password2', ['Обязательное поле.'])
        resp = self.client.post(reverse('register'), {'password2': '@'})
        self.assertFormError(resp, 'form', 'password2',
                             ['Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.'])
        resp = self.client.post(reverse('register'), {'password2': '12345678'})
        self.assertFormError(resp, 'form', 'password2', [
            'Введённый пароль слишком широко распространён.',
            'Введённый пароль состоит только из цифр.'
        ])
        resp = self.client.post(reverse('register'), {'password2': 'abcdefgh'})
        self.assertFormError(resp, 'form', 'password2', [
            'Введённый пароль слишком широко распространён.'
        ])
        resp = self.client.post(reverse('register'), {'password2': 'парольмаксима'})
        self.assertFormError(resp, 'form', 'password2', [])

    def test_form_passwords_do_not_match(self):
        resp = self.client.post(reverse('register'), {
            'username': 'Максим',
            'shelter': 2,
            'password1': '@',
            'password2': '$'
        })
        self.assertFormError(resp, 'form', 'password2', ['Введенные пароли не совпадают.'])

    def test_form_success_redirect(self):
        resp = self.client.post(reverse('register'), {
            'username': 'Максим',
            'shelter': 2,
            'password1': 'парольмаксима',
            'password2': 'парольмаксима'
        })
        self.assertRedirects(resp, reverse('login'))
        self.assertTrue(ShelterUser.objects.filter(username='Максим').exists())
        self.assertEqual(ShelterUser.objects.get(username='Максим').shelter.pk, 2)


class ShelterUserLoginViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ShelterUser.objects.create_user(username='Валера', password='парольвалеры')

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('login'))
        self.assertTemplateUsed(resp, 'shelter_app/login.html')

    def test_form_invalid(self):
        resp = self.client.post(reverse('login'), {
            'username': '',
            'password': '',
        })
        self.assertFormError(resp, 'form', 'username', ['Обязательное поле.'])
        self.assertFormError(resp, 'form', 'password', ['Обязательное поле.'])

        resp = self.client.post(reverse('login'), {
            'username': 'вАЛЕРА',
            'password': 'ПАРОЛЬВАЛЕРЫ',
        })
        self.assertContains(
            resp,
            'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'
        )

        resp = self.client.post(reverse('login'), {
            'username': 'Валера',
            'password': 'парольвани',
        })
        self.assertContains(
            resp,
            'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'
        )

        resp = self.client.post(reverse('login'), {
            'username': 'Максим',
            'password': 'парольмаксима',
        })
        self.assertContains(
            resp,
            'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'
        )

    def test_form_valid_redirect(self):
        resp = self.client.post(reverse('login'), {
            'username': 'Валера',
            'password': 'парольвалеры',
        })
        self.assertRedirects(resp, reverse('pets'))

# TODO убирай хардкод по максимуму!
