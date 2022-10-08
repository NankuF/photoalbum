# Фотоальбом
Тестовое задание на знание Django и DRF.
<details>
    <summary>Задание</summary>
Сделать фотоальбом на Django и DRF, покрыть тестами API запросы и модули - модульные и интеграционные тесты. Разработать только бэкенд-часть.

- Название главного модуля - "app".
- Должна быть стандартная админка Django.
- Безопасность - пользователи не должны видеть чужие альбомы.
- Регистрация и авторизация перед использованием, работа по токену.
- manage.py команда для первоначального заполнения данными.
- Файлы можно загружать не более определенного размера (5 мб) - форматы PNG (.png), JPEG (.jpg, *.jpeg).
- Для альбома и фото должны быть еще нередактируемые пользователем поля - дата создания, у альбома также - количество фотографий в альбоме, автор (ID). Эти поля также должны возвращаться из API.
- API методы должны начинаться с /api/v1/
- Методы API:
  - авторизация,
  - регистрация,
  - создать новый альбом (название), отредактировать альбом (название), получить список альбомов (возможные сортировки - по дате создания, по количеству фотографий в альбоме), получить один альбом, удалить альбом.
  - загрузить фотографию в альбом (название, список тегов, файл), изменить фотографию в альбоме (название, список тегов), удалить фотографию из альбома, получить список фотографий (возможные фильтры - альбом, тег, возможные сортировки - по дате, по альбому), получить фотографию.
- При запросе фотографий из альбома должны возвращаться не только оригинальные размеры, но и уменьшенные копии - 150 пикселей по бОльшей стороне.
- Подключить документацию DRF.
- Покрыть вышеперечисленное тестами.
- Должно проходить pylint (кодстайл должен быть pep8, ошибок не должно быть, coverage должен быть больше или равен 90%).
- Лицевую часть делать не надо - только REST и админка.
</details>

---
# Визуальная проверка
### Запуск
1. создать файл `.env` внутри `photoalbum/app/`
```text
SECRET_KEY=django-insecure-^dqzg8p!j@6gen7m7==43+9a9u^f_t$&_h5w1m)j5+8qlpq!g+
DEBUG=True
```
2. Выполнить последовательно команды
```commandline
pip install -r requirements.txt
```
```commandline
python manage.py makemigrations
```
```commandline
python manage.py migrate
```
```commandline
python manage.py fill_db
```
```commandline
python manage.py runserver
```
---
#### Вход через админку
login: admin<br>
password: 123
```commandline
http://127.0.0.1:8000/admin/
```
---
#### Вход через браузерный api
```commandline
http://127.0.0.1:8000/api/v1/
```
Нажать `login` и ввести логин и пароль для админа.

Чтобы войти под другим юзером необходимо:
1. Зайти в админку под админом.
2. Выбрать пользователя в разделе `Пользователи`.
3. Cменить пароль пользователю.
4. Разлогиниться
5. Войти под логином и паролем выбранного пользователя 
```text
http://127.0.0.1:8000/api/v1/
```
---
## Методы
### Регистрация
```text
curl -d "username=braundiane&password=zxcvbnm,./123" -X POST http://localhost:8000/api/v1/auth/users/
```
### Авторизация
**Запрос по этому адресу вернет токен авторизации, который необходимо использовать во всех дальнейших запросах.**
```text
curl -d "username=braundiane&password=zxcvbnm,./123" -X POST http://localhost:8000/auth/token/login/
```
В браузере можно залогиниться по этому адресу:
```text
http://127.0.0.1:8000/api/v1/drf-authlogin/
```

## Методы работы с альбомом
### Создать новый альбом
```text
curl -d "title=new" -H "Authorization:Token 1f375e908a531cb3ee8297ecbda433ef874b4832" -X POST http://127.0.0.1:8000/api/v1/albums/
```
### Список альбомов
```text
curl -H "Authorization:Token 1f375e908a531cb3ee8297ecbda433ef874b4832" http://localhost:8000/api/v1/albums/
```
### Список альбомов с сортировкой по убыванию даты создания
```text
curl -H "Authorization:Token 1f375e908a531cb3ee8297ecbda433ef874b4832" http://127.0.0.1:8000/api/v1/albums/?ordering=-created
```
Доступные варианты сортировки:<br>
`ordering=created` - по возрастанию<br>
`ordering=-created` - по убыванию<br>
`ordering=images_count` - кол-во фотографий по возрастанию<br>
`ordering=-images_count` - кол-во фотографий по убыванию<br>
Доступные варианты фильтрации:<br>
`created=04.10.2022`  - дата создания<br>
`created_gte=04.10.2022 14:55:01` - дата создания больше или равно<br>
`created_lte=` - дата создания меньше или равно<br>
`created_gt=` - дата создания больше чем<br>
`created_lt=` - дата создания меньше чем<br>
`images_count=1` - количество фото в альбоме<br>
`images_count_gte=` - Количество фото в альбоме больше или равно<br>
`images_count_lte=` - Количество фото в альбоме меньше или равно<br>
`images_count_gt=` - Количество фото в альбоме больше чем<br>
`images_count_lt=` - Количество фото в альбоме меньше чем<br>
### Список альбомов с сортировкой и фильтрацией
```text
curl -H "Authorization:Token 1f375e908a531cb3ee8297ecbda433ef874b4832" http://127.0.0.1:8000/api/v1/albums/?created=&created_gt=&created_gte=&created_lt=04.10.2022&ordering=created
```
### Получить один альбом
```text
curl -H "Authorization:Token 1f375e908a531cb3ee8297ecbda433ef874b4832" http://localhost:8000/api/v1/albums/25/
```
### Переименовать альбом
```text
curl -d "title=new_new" -H "Authorization:Token 1f375e908a531cb3ee8297ecbda433ef874b4832" -X PUT http://localhost:8000/api/v1/albums/25/
```
### Удалить альбом
```text
curl -H "Authorization:Token 1f375e908a531cb3ee8297ecbda433ef874b4832" -X DELETE http://localhost:8000/api/v1/albums/25/
```

## Методы работы с фотографией смотрите в документации swagger
```text
http://127.0.0.1:8000/swagger/
```
---
# Тесты
```commandline
coverage run manage.py test && coverage report
```
```text
Name                                         Stmts   Miss  Cover
----------------------------------------------------------------
app/__init__.py                                  0      0   100%
app/settings.py                                 29      0   100%
app/urls.py                                     16      1    94%
manage.py                                       12      2    83%
photoalbum/__init__.py                           0      0   100%
photoalbum/admin.py                             38     17    55%
photoalbum/apps.py                               6      0   100%
photoalbum/filters.py                           24      0   100%
photoalbum/management/__init__.py                0      0   100%
photoalbum/management/commands/__init__.py       0      0   100%
photoalbum/migrations/0001_initial.py            9      0   100%
photoalbum/migrations/__init__.py                0      0   100%
photoalbum/models.py                            65      9    86%
photoalbum/serializers.py                       19      3    84%
photoalbum/signals.py                           21      2    90%
photoalbum/tests.py                             94      0   100%
photoalbum/views.py                             25      1    96%
----------------------------------------------------------------
TOTAL                                          358     35    90%

```
