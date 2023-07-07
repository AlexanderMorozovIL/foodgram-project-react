# Foodgram «Продуктовый помощник»

Онлайн-сервис, позволяющим пользователям публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Полный список запросов и эндпоинтов описан в документации ReDoc, доступна после запуска проекта по адресу:

```
http://158.160.6.88/api/docs/
```

# Технологии:
    Django
    DjangoRestFramework
    Python
    PostgreSQL
    Docker

### Как запустить проект:

#### 1. Клонируем репозиторий на локальную машину:
```
https://github.com/AlexanderMorozovIL/foodgram-project-react
git clone git@github.com:AlexanderMorozovIL/foodgram-project-react.git
```

#### 2. Создать файл ```.env``` в папке проекта _/infra/_ и заполнить его всеми ключами:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=f00dgram
DB_HOST=db
DB_PORT=5432
DJANGO_SECRET_KEY=<ваш_django_секретный_ключ>
```
Вы можете сгенерировать ```DJANGO_SECRET_KEY``` следующим образом.
Из директории проекта _/backend/_ выполнить:
```python
python manage.py shell
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```
Полученный ключ скопировать в ```.env```.

#### 3. Запуск Docker контейнеров: Запустите docker-compose
```
cd infra/
docker-compose up -d --build
```

#### 4. Сделать миграции, собрать статику и создать суперпользователя:
```
docker-compose exec -T web python manage.py makemigrations
docker-compose exec -T web python manage.py migrate
docker-compose exec -T web python manage.py collectstatic --no-input
docker-compose exec web python manage.py createsuperuser
```

Чтобы заполнить базу данных начальными данными списка ингридиетов выполните:
```
docker-compose exec -T backend python manage.py loaddata data.json
```

#### 5. Проверьте доступность сервиса
```
http://localhost/admin
```

### Документация
```
http://localhost/api/docs/
```


Автор:
```
https://github.com/AlexanderMorozovIL - Александр Морозов
```
