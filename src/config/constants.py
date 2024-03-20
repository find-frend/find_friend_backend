from config import settings


class Messages(object):
    """Сообщения."""

    EMAIL_ENGLISH_ONLY_MSG = (
        "Почта должна содержать буквы только английского алфавита."
    )
    INVALID_SYMBOLS_MSG = "Введены недопустимые символы."
    EMPTY_FIELD_MSG = "Поле не может быть пустым."
    PASSWORD_LENGTH_MSG = (
        f"Пароль должен содержать от {settings.MIN_LENGTH_PASSWORD} "
        f"до {settings.MAX_LENGTH_PASSWORD} символов."
    )
    INVALID_CREDENTIALS_MSG = "Неверные имя пользователя или пароль."
    INVALID_EMAIL_MSG = "Некорректный адрес электронной почты."
    FIRST_NAME_LENGTH_MSG = (
        f"Имя должно содержать от {settings.MIN_LENGTH_CHAR} до "
        f"{settings.MAX_LENGTH_CHAR} символов."
    )
    LAST_NAME_LENGTH_MSG = (
        f"Фамилия должна содержать от {settings.MIN_LENGTH_CHAR} до "
        f"{settings.MAX_LENGTH_CHAR} символов."
    )
    EMAIL_LENGTH_MSG = (
        f"Почта должна содержать от {settings.MIN_LENGTH_EMAIL} до "
        f"{settings.MAX_LENGTH_EMAIL} символов."
    )
    CANNOT_START_CHAT_WITH_NONEXISTENT_USER = (
        "Нельзя начать чат с несуществующим пользователем."
    )
    CHAT_DOES_NOT_EXIST = "Такого чата не существует."
    USER_NOT_ALLOWED_TO_VIEW_CHAT = "Вы не можете просматривать этот чат."


messages = Messages()
