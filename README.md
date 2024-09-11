![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)

## Описание проекта

Проект: Простое клиент-серверное приложение для хранения данных
Этот проект представляет собой простое клиент-серверное приложение, позволяющее пользователям загружать и скачивать файлы через REST API. Проект создан для демонстрации базового сервиса хранения данных, где пользователи могут взаимодействовать с сервером для управления своими файлами. Проект выполнен с учетом того, что пользователь может попытаться загрузить очень большой файл, который не стоит читать в память полностью.


### Технологии

- Python 3.9
- FastAPI
- SqlAlchemy


### Запуск проекта

Клонировать репозиторий и перейти в него в командной строке: 
```
git clone github.com/LenarSag/test_task_file_storage
```
Cоздать и активировать виртуальное окружение: 
```
python3.9 -m venv venv 
```
* Если у вас Linux/macOS 

    ```
    source venv/bin/activate
    ```
* Если у вас windows 
 
    ```
    source venv/Scripts/activate
    ```
```
python3.9 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Запуск проекта:
```
python main.py
```

Документация доступна после запуска по адресу:

http://127.0.0.1:8000/docs

### Как загружать файлы через Postman

Откройте Postman: запустите Postman и откройте новую вкладку или существующую.

Выберите метод HTTP: выберите POST в качестве метода HTTP.

Установите URL-адрес запроса: введите URL-адрес конечной точки FastAPI: http://127.0.0.1:8000/api/v1/files/upload

Перейдите на вкладку «Body»:

Выберите вкладку «Body» под строкой URL-адреса.
Выберите form-data.

Добавить файл в запрос:

В разделе form-data щелкните поле «Key» и введите имя поля файла (file, которое должно совпадать с именем параметра в маршруте FastAPI).
Щелкните раскрывающийся список справа от ключа и измените его с «text» на «file».

В поле «Значение» щелкните «Choose file» и выберите файл, который вы хотите загрузить с вашего компьютера.

Пример POST запроса для создания пользователя:

http://127.0.0.1:8000/api/v1/auth/users

```json
{
  "email": "user@example.com",
  "password": "string",
  "username": "user"
}
```

Ответ:
```json
{
  "id": 0,
  "username": "string",
  "email": "user@example.com"
}
```


Пример POST запроса для получения токена пользователя:

http://127.0.0.1:8000/api/v1/auth/token/login

```json
{
  "email": "user@example.com",
  "password": "string"
}
```

```json
 {
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImV4cCI6MTcyNjEyMjQ5OX0.VY92az_Ppj7pmtAPqlg9V2HWyz-aBHInIXQdK-KAK40",
  "token_type": "Bearer"
}
```

Пример POST запроса на загрузку файла на сервер:

http://127.0.0.1:8000/api/v1/files/upload


```json
{
    "unique_filename": "4f35a1b4-3e97-43c1-9a11-d32a72f32fa4",
    "filename": "beginner.pdf",
    "size": 793169,
    "content_type": "application/pdf",
    "id": 7,
    "created_at": "2024-09-11T04:12:46",
    "user_id": 1
}
```

Пример GET запроса на получения списка данных всех файлов:

http://127.0.0.1:8000/api/v1/files

```json
{
    "items": [
        {
            "unique_filename": "655604e8-fced-45f4-8117-63df9aca54c9",
            "filename": "1.pdf",
            "size": 257975,
            "content_type": "application/pdf",
            "id": 1,
            "created_at": "2024-09-11T03:28:54",
            "user_id": 1
        },
        {
            "unique_filename": "9174d610-ac86-403b-8489-6351825b3549",
            "filename": "fun,wmv",
            "size": 288674975,
            "content_type": "video/x-ms-wmv",
            "id": 2,
            "created_at": "2024-09-11T03:36:02",
            "user_id": 1
        },
        {
            "unique_filename": "a1646995-4f1d-4dd3-b999-a51e5221822b",
            "filename": "1",
            "size": 257975,
            "content_type": "application/octet-stream",
            "id": 3,
            "created_at": "2024-09-11T03:39:27",
            "user_id": 1
        },
    ],
    "total": 3,
    "page": 1,
    "size": 50,
    "pages": 1
}
```


Пример GET запроса на получения списка данных всех файлов пользователя:

http://127.0.0.1:8000/api/v1/files/me

```json

{
    "items": [
        {
            "unique_filename": "655604e8-fced-45f4-8117-63df9aca54c9",
            "filename": "1",
            "size": 257975,
            "content_type": "application/octet-stream",
            "id": 1,
            "created_at": "2024-09-11T03:28:54",
            "user_id": 1
        },
        {
            "unique_filename": "9174d610-ac86-403b-8489-6351825b3549",
            "filename": "1",
            "size": 257975,
            "content_type": "application/octet-stream",
            "id": 2,
            "created_at": "2024-09-11T03:36:02",
            "user_id": 1
        },
    ],
    "total": 2,
    "page": 1,
    "size": 50,
    "pages": 1
}
```

Пример GET запроса на получения данных конкретного файла:

http://127.0.0.1:8000/api/v1/files/655604e8-fced-45f4-8117-63df9aca54c9

```json
{
    "unique_filename": "655604e8-fced-45f4-8117-63df9aca54c9",
    "filename": "1",
    "size": 257975,
    "content_type": "application/octet-stream",
    "id": 1,
    "created_at": "2024-09-11T03:28:54",
    "user_id": 1
}
```

Пример GET запроса на скачивание файла:

http://127.0.0.1:8000/api/v1/files/2c885614-59d4-4458-be12-93b5f1064009/download


Пример DELETE запроса на удаление файла(можно удалять только свои файлф):

http://127.0.0.1:8000/api/v1/files/2c885614-59d4-4458-be12-93b5f1064009