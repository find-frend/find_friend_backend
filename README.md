![workflow](https://github.com/find-frend/find_friend_backend/actions/workflows/find_friend_workflow.yml/badge.svg)

# Бэкенд приложения "Найди друга"

Знакомства с новыми людьми, поиск людей с общими интересами и организация совместных мероприятий

## Структура проекта:

| Имя   | Описание                                                  |
| ----- | --------------------------------------------------------- |
| src   | Файлы для backend разработки                              |
| infra | Docker-compose файлы для запуска проекта с помощью Docker |

## Подключенные приложения:

1. Users - отвечает за создание пользователей
2. Api - вспомогательное приложение для api

## Правила работы с git (как делать коммиты и pull request-ы):

1. Две основные ветки: `main` и `develop`
2. Ветка `develop` — “предрелизная”. Т.е. здесь должен быть рабочий и выверенный код
3. В `main` находится только production-ready код (CI/CD)
4. Создавая новую ветку, наследуйтесь от ветки `develop`
5. Правила именования веток
   - весь новый функционал — `feature/название-функционала`
   - исправление ошибок — `bugfix/название-багфикса`
6. Пушим свою ветку в репозиторий и открываем Pull Request

## Добавление пакетов в requireremens.txt

При установке пакетов не забывайте добавлять их в requirements.txt!
Если устанавливаемый вами пакет нужен только на этапе разработки и не требуеся на боевом сервере, прописывайте зависимость в requirements-**dev**.txt!

## Запуск приложения:

**!!! ИНСТРУКЦИЯ ДЛЯ ЭТАПА РАЗРАБОТКИ !!!**

Для локальной разработки нужно:

1. Клонировать репозиторий и перейти в директорию:

```
git clone git@github.com:find-frend/find_friend_backend.git
```

```
cd find_friend_backend/
```

2. Создать и активировать виртуальное окружение:

```
python -m venv venv                      # Устанавливаем виртуальное окружение
source venv/scripts/activate             # Активируем (Windows); или
source venv/bin/activate                 # Активируем (Linux)
python -m pip install --upgrade pip      # Обновляем менеджер пакетов pip
pip install -r src/requirements-dev.txt  # Устанавливаем пакеты для разработки
```

3. Установить пре-коммит хуки:

```
pre-commit install
```

4. Создать файл `.env` с переменными окружения из `.env.example`. Пример наполнения - непосредственно в `.env.example`. Значение DEBUG при локальной разработке (в т.ч. для запуска дев сервера через python manage.py runserver) должно быть `True.`Для локальной разработки параметры DB не нужны, т.к. используется SQLite. Параметр `DJANGO_ALLOWED_HOSTS` можно закомментировать. Вот как выглядит `.env` для разработки:

```
DEBUG=True
DJANGO_SECRET_KEY=somegeneratedsecretkey
```

---

Для запуска приложения в контейнерах необходимо:

1. Заполнить `.env`:

```
DEBUG=False

DJANGO_SECRET_KEY=somegeneratedsecretkey

# Выставляем так, как ниже
DJANGO_ALLOWED_HOSTS=127.0.0.1 localhost backend

DB_ENGINE=django.db.backends.postgresql_psycopg2
POSTGRES_DB=findafriend
POSTGRES_USER=postgresusername
POSTGRES_PASSWORD=postgresuserpassword
DB_HOST=db
DB_PORT=5432
```

2. Перейти в директорию с файлом _docker-compose.dev.yaml_, открыть терминал и запустить docker-compose с ключом `-d`:

```
cd infra/dev/
```

```
docker compose -f docker-compose.dev.yaml up -d
```

3. Выполнить миграции:

```
docker compose -f docker-compose.dev.yaml exec backend python manage.py migrate
```

4. Создать суперюзера:

```
docker compose -f docker-compose.dev.yaml exec backend python manage.py createsuperuser
```

5. Собрать статику:

```
docker compose -f docker-compose.dev.yaml exec backend python manage.py collectstatic --no-input
```

6. После успешного запуска проект станет доступен по адресу:
   http://localhost/api - Корень api
   http://localhost/admin - Админка Django

7. Остановить проект:

```
docker compose -f docker-compose.dev.yaml down
```

8. Если необходимо пересобрать контейнеры после изменений в проекте:

```
docker compose -f docker-compose.dev.yaml up -d --build
```

## Регистрация и авторизация пользователей

Авторизация реализована с помощью токенов: пользователь регистрируется с емейлом и паролем, отдельным запросом получает токен, затем этот токен передаётся в заголовке каждого запроса.

Уровни доступа пользователей:

- Гость (неавторизованный пользователь)
- Авторизованный пользователь
- Администратор

Что могут делать неавторизованные пользователи
- Создать аккаунт.
  Что могут делать авторизованные пользователи
- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Менять свой пароль.

Что может делать администратор
Администратор обладает всеми правами авторизованного пользователя.
Плюс к этому он может:
- изменять пароль любого пользователя,
- создавать/блокировать/удалять аккаунты пользователей,

Эти функции реализованы в стандартной админ-панели Django.

_*Спецификации API в файле `openapi-schema.yml` в папке `docs`*_

Также документация API доступна по адресам:

- JSON - `/swagger.json`
- YAML - `/swagger.yaml`
- Swagger UI - `/swagger/`
- ReDoc UI - `/redoc/`

## Чат

Чат реализован на веб-сокетах для поддержки двухстороннего обмена данными с клиентом и асинхронных расширениях Django Channels для создания таких каналов передачи информации.

Использование веб-сокетов предполагает поддержку асинхронных вызовов со стороны процесса, обрабатывающего веб-запросы, поэтому для публикации используется протокол asgi. В нашем случае мы используем сервер daphne.

### Эндпоинты и логика

Доступны следующие эндпоинты:

#### Стандартные HTTP эндпоинты, обрабатываются WSGI сервером:

- `/api/v1/chats/start/` - **POST**, создание нового чата. Принимает email пользователя, с которым мы хотим начать чат. Пример:
```JSON
{"email": "myfriend@example.com"}
```
> Перед созданием чата проходят проверки:
> - Пользователь должен быть аутентифицирован
> - Если пользователь, ассоциированный с передаваемым email'ом, не является другом инициатора чата, выводится сообщение "`Чтобы начать чат, вы должны быть в друзьях с пользователем Имя Фамилия."`
> - Если пользователя с такой почтой нет, выводится сообщение "`Нельзя начать чат с несуществующим пользователем."`
> - Если чат между указанными пользователями уже существует, происходит автоматическая переадресация на эндпоинт `/api/v1/chats/<id>`
> - Если же всё ок и такого чата ещё нет, происходит его создание и выводится информация о чате - его id, инициатор и получатель, а также список сообщений в чате (по умолчанию выводится 30 сообщений, число настраивается). Пример ответа при создании:

```JSON
{
    "id": 3,
    "initiator": {
        "email": "testuser1@fake.org",
        "first_name": "Тестодин",
        "last_name": "Юзеродин",
        "age": 23,
        "city": null
    },
    "receiver": {
        "email": "testuser2@fake.org",
        "first_name": "Тестдва",
        "last_name": "Юзердва",
        "age": 23,
        "city": null
    },
    "chat_messages": []
}
```

- `/api/v1/chats/<id>` - **GET**, просмотр информации о чате. Доступен только пользователям, являющимся участниками чата, а также админам. Пример ответа:
```JSON
{
    "id": 3,
    "initiator": {
        "email": "testuser1@fake.org",
        "first_name": "Тестодин",
        "last_name": "Юзеродин",
        "age": 23,
        "city": null
    },
    "receiver": {
        "email": "testuser2@fake.org",
        "first_name": "Тестдва",
        "last_name": "Юзердва",
        "age": 23,
        "city": null
    },
    "chat_messages": [
        {
            "id": 7,
            "sender": 19,
            "text": "Ну привет, коль не шутишь!",
            "timestamp": "2024-03-21T11:07:23.587564+03:00"
        },
        {
            "id": 6,
            "sender": 18,
            "text": "Привет!",
            "timestamp": "2024-03-21T11:07:10.565906+03:00"
        }
    ]
}
```

- - `/api/v1/chats/` - **GET**, список чатов. Пример ответа:
```JSON
[
    {
        "id": 3,
        "initiator": {
            "email": "testuser1@fake.org",
            "first_name": "Тестодин",
            "last_name": "Юзеродин",
            "age": 23,
            "city": null
        },
        "receiver": {
            "email": "testuser2@fake.org",
            "first_name": "Тестдва",
            "last_name": "Юзердва",
            "age": 23,
            "city": null
        },
        "start_time": "2024-03-20T10:26:23.028760+03:00",
        "last_message": {
            "id": 7,
            "sender": 19,
            "text": "Ну привет, коль не шутишь!",
            "timestamp": "2024-03-21T11:07:23.587564+03:00"
        }
    },
    {
        "id": 4,
        "initiator": {
            "email": "testuser1@fake.org",
            "first_name": "Тестодин",
            "last_name": "Юзеродин",
            "age": 23,
            "city": null
        },
        "receiver": {
            "email": "admin@fake.org",
            "first_name": "Админ",
            "last_name": "Админов",
            "age": null,
            "city": null
        },
        "start_time": "2024-03-20T13:26:01.689827+03:00",
        "last_message": null
    }
]
```

#### Websocket эндпоинт, обрабатывается ASGI сервером:

- `/ws/chat/<room_name>`. В логике нашего приложения `room_name` - это `chat_id`, который присваивается чату при его создании.

При подключении к чату из базы подгружаются последние сообщения в чате (по умолчниаю 30, число настраивается).

### Тестирование работы чатов

Прежде всего необходимо, чтобы в базе были два пользователя с токенами аутентификации. Эти пользователи должны быть в друзьях друг у друга. Для примера user1@fake.org и user2@fake.org. Затем нужно создать новый чат (см. выше) - будучи залогиненным как `user1`, отправить POST запрос на `/api/v1/chats/start/` с email'ом `user2`. После получения id чата можно приступать к тестированию непосредственно чата на вебсокете.

Для тестирования будем использовать [Postman](https://www.postman.com/downloads/).

Начнем с создания нового запроса:
[Imgur](https://imgur.com/jwLwxoo)

По умолчанию создается HTTP запрос. Необходимо изменить тип на Websocket:
[Imgur](https://imgur.com/yvy9JtE)

Сохраняем запрос: `Save` -> Request name "User 1" -> Внизу слева `New Collection` -> Название коллекции "Find Friend" -> `Save`.

Коллекция появляется в списке коллекций, в ней пока один запрос `User 1`.

Нажимаем на коллекцию, котрывается окно с двумя вкладками: Overview и Variables. Нам нужна вкладка Variables. Там добавляем новую переменную baseUrl, в Initial value и Current value прописываем `ws://127.0.0.1:8000/ws/chat`. Сохраняем (`Ctrl` + `S`).

Прописываем еще две переменных - `authToken1` и `authToken2`. Значениями должны быть токены аутентификации, полученные при создании юзеров. Сохраняем.

Должно получиться вот так:
[Imgur](https://imgur.com/iYIEa58)

Теперь настроим запрос `User 1`.

В поле Enter URL вводим `{{baseUrl}}/1/` (где `1` - это id чата, присвоенный ему базой данный при создании чата).

Переходим на вкладку Headers, добавляем новый Key `Authorization` со значением `Token {{authToken1}}`. Сохраняем (`Ctrl` + `S`).

Теперь делаем дубликат запроса и переименовываем его в `User 2`(правой кнопкой по запросу -> `Duplicate` -> Правой кнопкой по дубликату -> `Rename`).

В настроках `User 2` переходим в Headers, меняем Value на `Token {{authToken2}}`, сохраняем (`Ctrl` + `S`).

Запускаем локальный dev-сервер (`python manage.py runserver`), если еще не запущен. При запуске в логах должна быть срочка `Starting ASGI/Daphne version 4.1.0 development server at http://127.0.0.1:8000/`. Это свидетельствует о том, что командой runserver теперь управляет daphne, что и позволит нам установить websocket соединение.

Теперь в обоих запросах нажимаем на кнопку Connect. Внизу в разделе Response для обоих юзеров должно отобразиться `Connected to ws://127.0.0.1:8000/ws/chat/1/` с зеленой галочкой и статус Connected.

Теперь можно написать первое сообщение от имени User 1, любой текст (просто текст, не JSON), и нажать на кнопку Send. Сообщение появится внизу в разделе Response в виде JSON с id и прочими атрибутами. В этот момент оно уходит в базу.

Если теперь перейти в User 2, это сообщение появится и у него. Если появилось, значит, всё ОК. Можно поотправлять сообщения с разных юзеров, и они все должны появляться у обоих.

Можно теперь отключиться от вебсокета (кнопка `Disconnect`). При повторном подключении будут автоматически подгружены последние сообщения из базы, с обратной сортировкой по времени.
