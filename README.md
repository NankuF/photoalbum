# Фотоальбом (API и админка)"

Не забыть отправить .env в письме.

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

