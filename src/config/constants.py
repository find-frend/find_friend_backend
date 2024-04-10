from django.contrib.auth import password_validation as pv
from django.core.exceptions import ValidationError
from django.db.models.fields import Field as DjangoField
from djoser.constants import Messages as DjoserMessages

MIN_LENGTH_EMAIL = 5
MAX_LENGTH_EMAIL = 254
MIN_LENGTH_CHAR = 2
MAX_LENGTH_CHAR = 150
MAX_LENGTH_EVENT = 50
MIN_LENGTH_PASSWORD = 8
MAX_LENGTH_PASSWORD = 50
MAX_LENGTH_DESCRIBE = 500
MAX_FILE_SIZE = 8 * 1024 * 1024  # 8388608
MAX_FILE_SIZE_MB = 8
MAX_MESSAGES_IN_CHAT = 30
MAX_CHAT_MESSAGE_LENGTH = 1000
MIN_USER_AGE = 14
MAX_USER_AGE = 120
MAX_LENGTH_TEXT = 1000

MAX_DISTANCE = 500


class Messages(object):
    """Сообщения."""

    EMAIL_ENGLISH_ONLY_MSG = (
        "Почта должна содержать буквы только английского алфавита."
    )
    INVALID_SYMBOLS_MSG = "Введены недопустимые символы."
    EMPTY_FIELD_MSG = "Поле не может быть пустым."
    PASSWORD_LENGTH_MSG = (
        f"Пароль должен содержать от {MIN_LENGTH_PASSWORD} "
        f"до {MAX_LENGTH_PASSWORD} символов."
    )
    INVALID_CREDENTIALS_MSG = "Неверные имя пользователя или пароль."
    INVALID_EMAIL_MSG = "Некорректный адрес электронной почты."
    FIRST_NAME_LENGTH_MSG = (
        f"Имя должно содержать от {MIN_LENGTH_CHAR} до "
        f"{MAX_LENGTH_CHAR} символов."
    )
    LAST_NAME_LENGTH_MSG = (
        f"Фамилия должна содержать от {MIN_LENGTH_CHAR} до "
        f"{MAX_LENGTH_CHAR} символов."
    )
    EMAIL_LENGTH_MSG = (
        f"Почта должна содержать от {MIN_LENGTH_EMAIL} до "
        f"{MAX_LENGTH_EMAIL} символов."
    )
    LESS_THAN_MIN_AGE = (
        f"Указанный возраст меньше {MIN_USER_AGE} лет! "
        f"Проверьте дату рождения."
    )
    MORE_THAN_MAX_AGE = (
        f"Возраст больше {MAX_USER_AGE} лет! Проверьте дату рождения."
    )
    INVALID_BIRTHDAY = "Некорректная дата рождения."
    CANNOT_START_CHAT_WITH_NONEXISTENT_USER = (
        "Нельзя начать чат с несуществующим пользователем."
    )
    CHAT_DOES_NOT_EXIST = "Такого чата не существует."
    USER_NOT_ALLOWED_TO_VIEW_CHAT = "Вы не можете просматривать этот чат."
    USER_IS_NOT_FRIEND = (
        "Чтобы начать чат, вы должны быть в друзьях с пользователем %s."
    )

    # Ниже получаем стандартные сообщения валидации Django и других пакетов
    FIELD_CANNOT_BE_BLANK_MSG = DjangoField.default_error_messages["blank"]
    INVALID_CREDENTIALS_MSG = DjoserMessages.INVALID_CREDENTIALS_ERROR

    def _get_standard_message(self, validation_method, value):
        try:
            validation_method(value)
        except ValidationError as e:
            return e.message

    @property
    def password_numeric_msg(self):
        """Сообщение Django при попытке использовать пароль только из цифр."""
        obj = pv.NumericPasswordValidator()
        return self._get_standard_message(obj.validate, "81672049")

    @property
    def password_common_msg(self):
        """Сообщение Django при попытке ввести распространённый пароль."""
        obj = pv.CommonPasswordValidator()
        return self._get_standard_message(obj.validate, "qwerty123")


messages = Messages()
