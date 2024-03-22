import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR.parent / ".env"

LOG_DIR = os.getenv("LOG_DIR_PATH", None)
if not LOG_DIR:
    LOG_DIR = BASE_DIR / "logs"
    LOG_DIR.mkdir(exist_ok=True)

load_dotenv(ENV_FILE)

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = (
    ["127.0.0.1", "localhost", "158.160.60.2", "backend"]
    if DEBUG
    else os.getenv("DJANGO_ALLOWED_HOSTS", "localhost").split(" ")
)

ESSENTIAL_APPS = ("daphne",)

DJANGO_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)

THIRD_PARTY_APPS = (
    "rest_framework.authtoken",
    "rest_framework",
    "channels",
    "djoser",
    "django_rest_passwordreset",
    "drf_yasg",
    "django_filters",
    "admin_auto_filters",
)

LOCAL_APPS = (
    "api.apps.ApiConfig",
    "users.apps.UsersConfig",
    "events.apps.EventsConfig",
    "chat.apps.ChatConfig",
)

INSTALLED_APPS = ESSENTIAL_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

CSRF_TRUSTED_ORIGINS = [
    "http://*.localhost",
    "http://*.127.0.0.1",
    "https://*.localhost",
    "https://*.127.0.0.1",
    "https://*.158.160.60.2",
    "http://*.158.160.60.2",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

CUSTOM_LOGGER_NAME = os.getenv("CUSTOM_LOGGER_NAME", "find_friends")
DEFAULT_LOG_LEVEL = os.getenv(
    "DEBUG_LOG_LEVEL" if DEBUG else "PROD_LOG_LEVEL", "INFO"
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "name_upper": {
            "()": "config.logging.NameUpperFilter",
        },
    },
    "formatters": {
        "default": {
            "format": (
                "[{name_upper}] {levelname} {asctime} {name} "
                "{module}.{funcName}:{lineno:d} {message}"
            ),
            "style": "{",
        },
        "verbose": {
            "format": (
                "[{name_upper}] {levelname} {asctime} | Thread / Process: "
                "{threadName} {thread:d} {process:d} | Logger: {name} "
                "File: {filename} Module/function/line: "
                "{module}.{funcName}:{lineno:d} | {message}"
            ),
            "style": "{",
        },
    },
    "handlers": {
        "console_handler": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["name_upper"],
            "formatter": "default",
        },
        "file_handler": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filters": ["name_upper"],
            "filename": f"{LOG_DIR}/{CUSTOM_LOGGER_NAME}.log",
            "mode": "a",
            "encoding": "utf-8",
            "formatter": "verbose",
            "backupCount": int(os.getenv("LOG_FILES_TO_KEEP", 5)),
            "maxBytes": int(os.getenv("LOG_FILE_SIZE", 1024 * 1024 * 10)),
        },
    },
    "loggers": {
        "": {
            "handlers": ["console_handler"],
            "level": DEFAULT_LOG_LEVEL,
        },
        "django": {
            "handlers": ["console_handler", "file_handler"],
            "level": DEFAULT_LOG_LEVEL,
            "propagate": False,
        },
        "daphne": {
            "handlers": ["console_handler", "file_handler"],
            "level": DEFAULT_LOG_LEVEL,
            "propagate": False,
        },
        CUSTOM_LOGGER_NAME: {
            "handlers": ["console_handler", "file_handler"],
            "level": DEFAULT_LOG_LEVEL,
            "propagate": False,
        },
    },
}


WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"


if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv(
                "DB_ENGINE", default="django.db.backends.postgresql"
            ),
            "NAME": os.getenv("POSTGRES_DB", default="postgres"),
            "USER": os.getenv("POSTGRES_USER", default="postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="postgrespswd"),
            "HOST": os.getenv("DB_HOST", default="db"),
            "PORT": os.getenv("DB_PORT", default="5432"),
        }
    }

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "users.validators.PasswordLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

DJOSER = {
    "SERIALIZERS": {
        "user": "api.serializers.MyUserSerializer",
        "user_create": "api.serializers.MyUserCreateSerializer",
        "current_user": "api.serializers.MyUserSerializer",
        "token_create": "api.serializers.CustomTokenCreateSerializer",
    },
    "PERMISSIONS": {
        "user": ["djoser.permissions.CurrentUserOrAdminOrReadOnly"],
        "user_list": ["rest_framework.permissions.IsAuthenticated"],
        "activation": ["rest_framework.permissions.IsAdminUser"],
    },
    "HIDE_USERS": False,
}

DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomNumberTokenGenerator",
    "OPTIONS": {
        "min_number": 100000,
        "max_number": 999999,
    },
}

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = BASE_DIR / "tmp/emails"
    DEFAULT_FROM_EMAIL = "local@example.com"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.yandex.ru"
    EMAIL_PORT = 465
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = True

    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    SERVER_EMAIL = EMAIL_HOST_USER
    EMAIL_ADMIN = EMAIL_HOST_USER

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (
                    "127.0.0.1" if DEBUG else os.getenv("REDIS_HOST", "redis"),
                    os.getenv("REDIS_PORT", 6379),
                )
            ],
        },
    },
}
