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

## Начало работы

1. Клонируйте репозиторий на локальную машину
```
git clone <адрес репозитория>
```
2. Для работы с проектом локально - установите вирутальное окружение и установите зависимости
```
python -m venv venv
pip install -r requirements.txt 
```
Для работы с проектом на удаленном сервере должен быть установлен Docker и docker-compose.
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
Загрузите последнюю версию Docker Compose с помощью следующей команды:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
Сделайте файл docker-compose исполняемым, выполнив команду:
```
sudo chmod +x /usr/local/bin/docker-compose
```
Чтобы проверить, что docker-compose установлен правильно, выполните команду:
```
docker-compose --version
```
Она должна вернуть версию установленного docker-compose

В репозитории на GitHub добавьте данные в `Settings - Secrets - Actions secrets`:
* DOCKER_PASSWORD, DOCKER_USERNAME - для работы с DockerHub 
* USER, HOST, PASSPHRASE, SSH_KEY - для подключения к удаленному серверу 


Скопируйте файлы из репозитория `docker-compose.yaml` и `nginx/default.conf` на сервер:

```
scp docker-compose.yaml <имя пользователя>@<имя сервера/ip-адрес>/home/<username>/docker-compose.yaml

scp default.conf <пользователя>@<имя сервера/ip-адрес>/home/<username>/default.conf
```
### После успешного деплоя:
Соберите статические файлы (статику):
```
docker-compose exec web python manage.py collectstatic --no-input
```
Примените миграции:
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate --noinput
```
Создайте суперпользователя
```
docker-compose exec backend python manage.py createsuperuser
```
Заполните базу ингредиентами
```
docker-compose exec backend python manage.py load_ingredients
```
### Проверьте работоспособность приложения, для этого перейдите на страницы:
`Админка`
[http://<ip-адрес сервера>/admin](http://51.250.90.191/admin)
(login: admin pass: admin)

`API`
[http://<ip-адрес сервера>/](http://51.250.90.191/api/)

`Сайт foodgram`
[http://<ip-адрес сервера>/](http://51.250.90.191/)








Автор: Варкулевич Михаил.
