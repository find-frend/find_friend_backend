# Бэкенд приложения "Найди друга" - Знакомства с новыми людьми, поиск людей с общими интересами и организация совместных мероприятий

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
cd infra/
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
