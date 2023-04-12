# Foodrgam
![Workflow Status](https://github.com/VarkulevichM/foodgram-project-react/actions/workflows/foodgram-project-react.yml/badge.svg)
Продуктовый помощник в котором реализованна работа сайта и API 
На этом сервисе пользователи смогут публиковать рецепты, подписываться на 
публикации других пользователей, добавлять понравившиеся рецепты в список 
«Избранное», а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.

### Технологии
- Python 
- Django 
- DRF 
- Docker
- Docker-compose
- PostgreSQL

### Что ещё не реализованно
- workflow
- И проект не развернут на удалённом сервере

## Начало работы

- Установите  docker и docker-compose.
- Создайте файл .env в корневой директории foodgram-project-react 
- Запустите команду `docker-compose up -d --buld`
- Примените миграции `'`docker-compose exec backend python manage.py migrate`'`
- Соберите статику `docker-compose exec backend python manage.py collectstatic --no-input`'`
- В базу данных можно загрузить ингредиенты командой: `docker-compose exec backend python manage.py load_ingredients`
- И создатей суперпользователя `docker-compose exec backend python manage.py createsuperuser`

`Работу сайта можно посмотреть тут:`
[http://localhost/recipes](http://localhost/recipes)

`Документация (запросы для работа с API):`
[http://localhost/api/docs/](http://localhost/api/docs/)


Автор: Варкулевич Михаил.