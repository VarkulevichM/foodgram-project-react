from django.core.exceptions import ValidationError


def validate_positive_cooking_time(value):
    if value <= 0:
        raise ValidationError(
            f"Конечно можно приготовить что-то за ноль минут,"
            f"но всё же давайте выставим время приготовления больше нуля."
            f"Вы ввели {value} измените это значение"
        )


def validate_positive_amount(amount):
    if amount <= 0:
        raise ValidationError(
            f"Приготовить из ничего, конечно неплохо, но всё-таки давайте "
            f"выставим количество ингредиентов больше нуля. Вы ввели {amount}"
            f" измените это значение"
        )
