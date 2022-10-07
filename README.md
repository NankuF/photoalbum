# Фотоальбом (API и админка)"

Не забыть отправить .env в письме.


### Регистрация
```text
curl -d "username=braundiane&password=zxcvbnm,./123" -X POST http://localhost:8000/api/v1/auth/users/
```
### Авторизация
POST запрос по этому адресу вернет токен авторизации, который необходимо использовать во всех запросах.
```text
curl -d "username=braundiane&password=zxcvbnm,./123" -X POST http://localhost:8000/auth/token/login/
```
Либо по этому адресу, если хотите посмотреть в браузере
```text
http://127.0.0.1:8000/api/v1/drf-authlogin/
```

### GET
```text
curl -H "Authorization:Token 8bd51a6423aa23f48cb260f105263f9c73ca8bed" http://localhost:8000/api/v1/albums/
```