"""Импорт csv-файлов из папки /data/load/."""

from csv import DictReader

from django.core.management import BaseCommand
from django.db import connection
from django.shortcuts import get_object_or_404

from chat.models import Chat, Message
from events.models import Event
from users.models import City, Interest, User

PARAMS_MODELS = {
    "cities": City,
    "interests": Interest,
    "users": User,
    "events": Event,
    "user_interest": (User, Interest),
    "chats": Chat,
    "messages": Message,
}

FIELDS = {
    "city": City,
    "user": User,
    "interest": Interest,
    "initiator": User,
    "receiver": User,
    "sender": User,
    "chat": Chat,
}


def change_foreign_keys(data_csv):
    """Изменяет значения внешних ключей при загрузке."""
    change_data = data_csv.copy()
    for key, value in data_csv.items():
        if key in FIELDS.keys():
            change_data[key] = FIELDS[key].objects.get(pk=value)
    return change_data


def reset_sequence(model):
    """Сброс последовательности id в таблице базы данных."""
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT setval('{table_name}_id_seq', "
            f"(SELECT MAX(id) FROM {table_name}) + 1);"
        )


class Command(BaseCommand):
    """Command."""

    def add_arguments(self, parser):
        """Добавление аргументов."""
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            default=False,
            help="Load all data to all models",
        )
        for param in PARAMS_MODELS.keys():
            parser.add_argument(
                f"--{param}",
                action="store_true",
                default=False,
                help=f"Load {param} data",
            )

    def _remove_auto_now_add(self, model_instance):
        for field in model_instance._meta.fields:
            try:
                if field.auto_now_add:
                    field.auto_now_add = False
            except AttributeError:
                continue
        return model_instance

    def _process_csv(self, file_name, model_name):
        """Обработка csv-файла."""
        with open(f"data/load/{file_name}", encoding="utf-8") as csvfile:
            for data_csv in DictReader(csvfile):
                row_data = change_foreign_keys(data_csv)
                try:
                    if file_name != "user_interest.csv":
                        ex_model = model_name(**row_data)

                        ex_model = self._remove_auto_now_add(ex_model)

                        ex_model.save()
                    else:
                        user_obj = get_object_or_404(User, id=data_csv["user"])
                        interest_obj = get_object_or_404(
                            Interest, id=data_csv["interest"]
                        )
                        user_obj.interests.add(interest_obj)
                        user_obj.save()

                except Exception as error:
                    self.stderr.write(self.style.WARNING(f"{error}"))
                    raise Exception(error)
            if (
                connection.vendor == "postgresql"
                and file_name != "user_interest.csv"
            ):
                reset_sequence(model_name)
            self.stdout.write(
                self.style.SUCCESS(f"Successfully load {file_name}")
            )

    def handle(self, *args, **options):
        """Handle."""
        if options["all"]:
            for param, model in PARAMS_MODELS.items():
                self._process_csv(f"{param}.csv", model)
        else:
            for param, model in PARAMS_MODELS.items():
                if options[param]:
                    self._process_csv(f"{param}.csv", model)
