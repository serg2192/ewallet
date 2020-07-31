**Запуск проекта**

В корне проекта выполнить:
```bash
docker-compose -f ./docker-compose.yaml up
```
Проект будет доступен на 0.0.0.0:8080

**Важные заметки по реализации:**
1. Все попытки вызова методов будут возвращать либо 200(с каким-либо кодом в metadata) 
либо 500(если возникло какое то исключение)
1. Данные хранятся в docker volume (db). 
Удалить будет необходимо самостоятельно.

Примеры успешных запросов

1. Метод создания кошелька(если баланс не передан, начальный баланс будет 0)
```bash
curl -w '\n' -iX POST 'http://0.0.0.0:8080/create_account' -H 'Content-Type:application/json' -d '{"balance":100.32}'
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 91
Date: Thu, 30 Jul 2020 21:35:32 GMT
Server: Python/3.7 aiohttp/3.6.2

{"data": {"user_id": 1}, "metadata": {"code": 0, "message": "Успех", "details": null}}
```

2. Добавить денег на счет
```bash
curl -w '\n' -iX POST 'http://0.0.0.0:8080/add_money' -H 'Content-Type:application/json' -d '{"user_id":1, "amount":143.25}'
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 81
Date: Thu, 30 Jul 2020 21:35:54 GMT
Server: Python/3.7 aiohttp/3.6.2

{"data": null, "metadata": {"code": 0, "message": "Успех", "details": null}}
```

3. Перевод между пользователями
```bash
curl -w '\n' -iX POST 'http://0.0.0.0:8080/transfer' -H 'Content-Type:application/json' -d '{"source_user_id":1,"target_user_id":2,"amount":100}'
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 81
Date: Thu, 30 Jul 2020 22:07:23 GMT
Server: Python/3.7 aiohttp/3.6.2

{"data": null, "metadata": {"code": 0, "message": "Успех", "details": null}}
```

4. Респонс в случае невалидных параметров унифицирован
```bash
curl -w '\n' -iX POST 'http://0.0.0.0:8080/add_money' -H 'Content-Type:application/json' -d '{"user_id":5}'
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 186
Date: Fri, 31 Jul 2020 20:07:59 GMT
Server: Python/3.7 aiohttp/3.6.2

{"data": null, "metadata": {"code": 100, "message": "Переданы неверные входные параметры", "details": [{"amount": ["Missing data for required field."]}]}}
```

