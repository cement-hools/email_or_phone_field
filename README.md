<!---
https://github.com/cement-hools/email_or_phone_field/badge.svg
--->
![example workflow](https://github.com/cement-hools/email_or_phone_field/actions/workflows/project_test.yml/badge.svg)
### Используется GitHub Actions для автоматического тестирования при изменении кода в репозитории

# email_or_phone_field
Разработать отказоустойчивый мини сервис, который принимает POST запросы 
в формате JSON с данными о пользователях и создаёт их в БД postgres 

## stack
- python 3.9
- django
- django REST framework
- PostgreSQL
- Docker-compose

### Регистрация и авторизация пользователя 
- **POST**```/useradd/``` Регистрация, передать JSON вида. 

Тебования:
- login:
  - Максимум 150 символов.
  - Буквы, цифры и только @/./+/ -/_.
- password:
   - Не должен совпадать с вашим именем или другой персональной информацией или быть слишком похожим на неё.
   - Должен содержать как минимум 8 символов.
   - Не может быть одним из широко распространённых паролей.
   - Не может состоять только из цифр
- У пользователя обязательно должен быть указан либо телефон либо почта. 
Может быть и телефон и почта одновременно.
```
{
    "name": "Sekachev Maxim Sergeevich", (обязательное поле: str)
    "date_of_birth": "09.02.1988", (необязательное: str)
    "phone": 9555666000, (условно обязательное: int)
    "email": "cement@ya.ru", (условно обязательное: str)
    "login": "cement" (обязательное поле: str)
}
``` 
При успешном запросе придет логин и пароль нового пользователя
```
{
    "login": "cement",
    "password": "YYjVHyJyMS"
}
```
- **POST**```/login/``` login, передать login и password
```
{
    "login": "cement",
    "password": "YYjVHyJyMS"
}
```
- **POST**```/logout/``` logout, отправить post запрос

### Статистика по запросам к /useradd/ (только для авторизованных пользователей)
- **GET**```/statistic/``` Статистика по успешным/не успешным запрсам в сервис /useradd со статусами операций и ошибками.
```
[
    {
        "create_date": "22.09.2021 15:52:00",
        "status": "HTTP_400_BAD_REQUEST",
        "text": "Обязательное поле (name), Пользователь с таким полем уже существует (login)"
    },
    {
        "create_date": "22.09.2021 15:23:58",
        "status": "HTTP_201_CREATED",
        "text": "Пользователь Sekachev Maxim Sergeevich успешно создан"
    },
    {
        "create_date": "22.09.2021 11:52:09",
        "status": "HTTP_400_BAD_REQUEST",
        "text": "Обязательное поле (date_of_birth, name, login)"
    }
]
```
- **GET**```/export_excel/``` экспорт статистики в xls
- **GET**```/export_txt/``` экспорт статистики в txt

## Установка и запуск на сервере разработчика
1. Клонировать репозиторий
    ```
    git clone https://github.com/cement-hools/email_or_phone_field
    ```
2. Перейдите в директорию crud_company
    ```
   cd email_or_phone_field
    ```
3. Создать виртуальное окружение, активировать и установить зависимости
    ``` 
   python -m venv venv
    ```
   Варианты активации окружения:
   - windows ``` venv/Scripts/activate ```
   - linux ``` venv/bin/activate ```
     <br><br>
   ```
   python -m pip install -U pip
   ```
   ```
   pip install -r requirements.txt
   ```
4. Выполните миграции
   ```
   python manage.py migrate
   ```
5. Создать суперюзера
   ```
   python manage.py createsuperuser
   ```
6. Запустить приложение на сервере разработчика
   ```
   python manage.py runserver
   ```
7. Проект доступен 
   ```
   http://localhost:8000/
   ```

## Тесты
```
python manage.py test
```

## Запуск в трех контейнерах (PostgreSQL, Web, Nginx)

1. Клонировать репозиторий
    ```
    git clone https://github.com/cement-hools/email_or_phone_field
    ```
2. Перейдите в директорию crud_company
    ```
   cd email_or_phone_field
    ```
3. Запустить docker-compose
    ```
    docker-compose up --build
    ```
4. Зайти в контейнер и выполнить миграции
    ```
    docker-compose exec web python manage.py migrate --noinput
    ```
5. Зайти в контейнер и создать суперюзера. Указать login, password
    ```
    docker-compose exec web python manage.py createsuperuser
    ```
7. Проект доступен 
   ```
   http://127.0.0.1/
   ```
