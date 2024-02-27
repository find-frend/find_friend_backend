"""Импорт csv-файлов из папки /data/load/."""

from csv import DictReader

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from events.models import Event
from users.models import City, Interest, User

PARAMS_MODELS = {
    "cities": City,
    "users": User,
    "interests": Interest,
    "events": Event,
    "user_interest": (User, Interest),
}

FIELDS = {
    "city": City,
    "user": User,
    "interest": Interest,
    "city": City,
}


def change_foreign_keys(data_csv):
    """Изменяет значения внешних ключей при загрузке."""
    change_data = data_csv.copy()
    for key, value in data_csv.items():
        if key in FIELDS.keys():
            change_data[key] = FIELDS[key].objects.get(pk=value)
    return change_data


class Command(BaseCommand):
    """Command."""

    def add_arguments(self, parser):
        """Добавление аргументов."""
        parser.add_argument(
            "--cities",
            action="store",
            help='Load data to "city" model',
        )
        parser.add_argument(
            "--interests",
            action="store",
            help='Load data to "interest" model',
        )
        parser.add_argument(
            "--users",
            action="store",
            help='Load data to "user" model',
        )
        parser.add_argument(
            "--events",
            action="store",
            help='Load data to "event" model',
        )

        parser.add_argument(
            "--user_interest",
            action="store",
            help='Load data to "userinterest" model',
        )

    def handle(self, *args, **options):
        """Handle."""
        for parameter, model_name in PARAMS_MODELS.items():
            if options[parameter]:

                with open(
                    f"data/load/{options[parameter]}", encoding="utf-8"
                ) as csvfile:
                    for data_csv in DictReader(csvfile):
                        data = change_foreign_keys(data_csv)
                        try:
                            if options[parameter] != "user_interest.csv":
                                ex_model = model_name(**data)
                                ex_model.save()
                            else:
                                user_obj = get_object_or_404(
                                    User, id=data_csv["user"]
                                )
                                interest_obj = get_object_or_404(
                                    Interest, id=data_csv["interest"]
                                )
                                user_obj.interests.add(interest_obj)
                                user_obj.save()
                        except Exception as error:
                            self.stderr.write(self.style.WARNING(f"{error}"))
                            raise Exception(error)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully load {options[parameter]}"
                        )
                    )
