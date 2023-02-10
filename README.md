# Shelter

## Описание
Добро пожаловать в мой пет-проект Shelter. Он представляет из себя веб-приложение для приютов домашних животных.
### Пользователи
- Доступ к контенту приложения имеют только зарегистрированные и авторизованные пользователи. При регистрации каждый из 
пользователей выбирает, к какому приюту он относится. Пользователь сможет взаимодействовать с объектами животных только 
из его приюта. Пользователи разделены на 3 тира: 'guest', 'user', 'admin'. Первые могут лишь просматривать объекты
животных, вторые также могут добавлять новых животных и редактировать информацию о существующих, третьи имеют право на
удаление объектов животных. При регистрации юзер причисляется к группе 'guest'. Добавить юзера в другую группу может
только суперюзер или другой юзер, имеющий доступ к административной части сайта.
### Животные
- Животные также как и юзеры прикреплены к определенному приюту. Они имеют параметры: кличка, рост, вес, дата рождения
(при просмотре этот параметр приобразуется в возраст животного), дата поступления в приют, вид (собака, кошка и тд), 
фотография, особые приметы. В приложении реализовано мягкое удаление животных. Если пользователь с правом 'admin'
удаляет животное, оно не удаляется из базы данных, а лишь перестает отображаться в клиентской части приложения.
Суперадмин или другой пользователь, имеющий доступ к административной части приложения, при необходимости может
восстановить удаленное животное.

## Пути
- '/' - главная страница сайта. Здесь отображается список животных из приюта текущего пользователя.
- '/pets/<id животного>' - страница животного. Здесь отображается подробная информация о животном.
- '/pet_create' - страница создания нового животного.
- '/pets/<id животного>/update' - страница обновления информации о животном.
*Функция удаления животного реализована через модальное окно. Ссылка для его вызова есть на странице со списком 
животных и на странице конкретного животного*
- '/register/' - страница регистрации нового пользователя.
- '/login/' - страница авторизации пользователя.

## API
Тажке в приложении реализовано api. Доступ к нему можно получить через путь '/api/'
- '/api/pet/' - страница со списком животных. Здесь же реализована функция добавления нового животного. Добавить 
животное можно через POST-запрос, указав все обязательные параметры.
- '/api/pet/<id животного>' - страница с информацией о конкретном животном. Здесь же реализованы функции обновления информации о 
животном и удаления животного. Сделать это можно через POST и DELETE запрос соответственно.
- 'api/registration/' - страница регистрации нового пользователя. Принимает только POST-ЗАПРОСЫ с данными для
регистрации.

## Установка
1. Копирование проекта: `git clone https://github.com/sergeytompson/shelter`
2. Переходим в папку проекта: `cd shelter`
3. Устанавливаем зависимости: `pip install -r requirements.txt`
4. Переходим в папку приложения: `cd shelter`
5. Создаем файл '.env' в котором прописываем:
   + SECRET_KEY=<секретный ключ Django>. Сгенерировать его можно через функцию `get_random_secret_key()` из модуля 
   django.core.management.utils
   + DB_ADMIN=<имя администратора нашей базы данных>
   + DB_PASSWORD=<ароль администратора нашей базы данных>
6. Убедитесь, что у вас установлена PostgreSQL. Создайте базу данных с именем 'shelter'. Как это сделать, можно узнать
в официальной [документации](https://postgrespro.ru/docs/postgresql/9.5/manage-ag-createdb). Убедитесь, что
администратор, чьи имя и пароль мы записали в прошлом шаге, имеет все права для работы с БД 'shelter'.
7. Выполните миграции: `python manage.py migrate`
8. (необязательно) Установите фикстуры: `python manage.py loaddata shelter_fixtures.json`. Фикстуры содержат 
приюты (5 шт), виды животных (5 шт), пользователей (10 шт) и питомцев (25 шт).
9. Запустите приложение: `python manage.py runserver`
10. Теперь наше приложение работает. Вам также может понадобиться создать суперпользователя для работы с 
административной частью сайта: `python manage.py createsuperuser` (вводить почту необязательно).

## Контакты
+ Telegram: @sergeytompson
+ Email: gfhfahfp@gmail.com