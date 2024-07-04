# Практика. 1

Через вирт. окружение установить Flask

создать файл app.py и добавить туда такой код:

```
from flask import Flask
app = Flask(__name__)
USERS = [
 {"id": 1, "name": "Ashley W. Walker", "phone": "317-769-0638", "birthday": "August 12, 1999", "email": "AshleyWWalker@dayrep.com", "username": "Joull1999"},
 {"id": 2, "name": "Martin M. Johnson", "phone": "301-962-1329", "birthday": "March 20, 1964", "email": "MartinMJohnson@teleworm.us", "username": "Youde1964"},
 {"id": 3, "name": "Justina D. Wallace", "phone": "914-819-0493", "birthday": "May 18, 1994", "email": "JustinaDWallace@rhyta.com", "username": "Donfe1994"},
 {"id": 4, "name": "Jason R. King", "phone": "608-562-1533", "birthday": "February 18, 1962", "email": "JasonRKing@dayrep.com", "username": "Ginusbact"},
 {"id": 5, "name": "Leroy T. Evans", "phone": "337-570-9574", "birthday": "January 7, 1946", "email": "LeroyTEvans@armyspy.com", "username": "Atiousaing"},
]
@app.route("/")
def hello_world():
 return "<p>Hello, World!</p>"
запускать командой
flask run --debug
```

Читаем документацию:
https://flask.palletsprojects.com/en/3.0.x/installation/
https://flask.palletsprojects.com/en/3.0.x/quickstart/#about-responses
https://flask.palletsprojects.com/en/3.0.x/quickstart/#rendering-templates


Выполнить задачи:

1. создать GET маршрут (название придумайте сами), подключить шаблонизатор и вывести всех пользователей в таблицу
2. создать POST маршрут (название придумайте сами), в тело запроса передается цифра, сервер должен вернуть информацию в формате json
т.е сервер получает от пользователя число, возводит его в квадрат и возвращает json ответ

формат запроса (x-www-form-urlencoded)
number=5
формат ответа (json):
{
 data: {
 "answer": 25
 }
}

выполнение 2ой задачи проверяем через POSTMAN

https://www.postman.com/downloads/
(регистрироваться не нужно)

смотрите скриншот постмана, x-www-form-urlencoded, это условно формат html формы
https://i.gyazo.com/cda4aa85a28794ae603a6e61466f8145.png

3. создать GET маршрут (название придумайте сами)
например
/users-list

в параметрах query, передаем ключ 'format'

Т.е вот так:

/users-list?format=json
/users-list?format=xml

если format == json
то возвращаем json

если format == xml
то возвращаем xml

работаем с массивом(list) USERS

можно использовать библиотеку dicttoxml, для преобразования массива в xml
https://pypi.org/project/dicttoxml/

смотрим в браузере или в постмане

4.
практически тоже самое что и в задаче 3

также создаем GET маршрут, но в этом случае, не обращаем внимания на GET параметры, а используем HTTP заголовок Accept

Тестируем через POSTMAN!

если клиент отправляет запрос с заголовком
Accept = application/json
то вернуть json

если клиент отправляет запрос с заголовком
Accept = application/xml
то вернуть xml

если у клиента тип контента не совпадает с application/json или с application/xml
то вернуть ошибку 404

заголовки указываем в табе Headers
https://i.gyazo.com/735380897b05c844781981e1e616abf7.png

5.через postman создать пользователя
маршрут можете придумать свой:

POST /users
тело отправляем в json, например
https://i.gyazo.com/cbcc455194829d5b52420e1c0e5fa79f.png

нужно создать и вернуть созданного пользователя в json
код ответе 201

данные добавляем в массив USERS

(если перейти к шагу 1 и открыть страницу с таблицей - увидим нового пользователя)

6. через postman удалить пользователя
маршрут можете придумать свой:

DELETE /users/{id}

где id, идентификатор пользователя

вернуть статус ответа 204, при последующих запросах также возвращается статус 204

7. через postman обновить пользователя
маршрут можете придумать свой:

PUT /users/{id}
где id, идентификатор пользователя

вернуть json обновленного пользователя, статус 200

в тело запроса передаем все данные

```
{
 "name": "Новое Имя",
 "phone": "Новый Телефон",
 "birthday": "Новое Дата рождения",
 "email": "Новый Email",
 "username": "Новый username"
}
```

8. через postman обновить пользователя
маршрут можете придумать свой:

PATCH /users/{id}
где id, идентификатор пользователя

вернуть json обновленного пользователя, статус 200

тело запроса от КЛИЕНТА может быть таким
```
{
 "name": "Новое имя",
 "phone": "Новый телефон",
}
таким
{
 "name": "Новое имя",
}
```
и т.д