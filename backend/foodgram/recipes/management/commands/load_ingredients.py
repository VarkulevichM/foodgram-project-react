import json
import os

from django.core.management.base import BaseCommand

from foodgram.settings import BASE_DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Загрузка ингредиентов из JSON файла"

    def add_arguments(self, parser):
        parser.add_argument("--json", type=str)

    def handle(self, *args, **options):
        json_file = os.path.join(BASE_DIR, "ingredients.json")

        if json_file:

            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

                for item in data:
                    ingredient = Ingredient(
                        name=item["name"],
                        measurement_unit=item["measurement_unit"])
                    ingredient.save()

            self.stdout.write(self.style.SUCCESS(
                "Загрузка ингредиентов из файла JSON завершена")
            )

        else:
            self.stdout.write(self.style.ERROR(
                "Файл JSON не найден")
            )
