# Фотоальбом (API и админка)"

Не забыть отправить .env в письме.


### Регистрация
```text
curl -d "username=user1&password=myverystrongpass123" -X POST http://localhost:8000/api/v1/auth/users/
```
### Авторизация
```text
curl -d "username=user1&password=myverystrongpass123" -X POST http://localhost:8000/auth/token/login/
```
POST запрос по этому адресу вернет токен авторизации, который необходимо использовать во всех запросах.
### GET
```text
curl -H "Authorization:Token f52554265eb86509a39d99eb1aa884900df22c65" http://localhost:8000/api/v1/albums/
```