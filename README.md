# praktikum_new_diplom
# Foodgram
«Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 
### Ссылка на проект
[Foodgram](https://foodgrampract.hopto.org/)

### Стек технологий использованный в проекте:
-   Django
-   Django REST Framework 
-   React
-   JS
-   Nginx
-   Gunicron
-   Docker

## Запуск проекта
1. Соберите контейнеры:
```
docker-compose up -d
```
2. Выполните миграции:
```
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```
3. Соберите и скопируйте статику:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```

## Создать юзера для админки:
```
docker compose exec backend python manage.py createsuperuser
```

## Импортировать данные из фикстур в БД:
```
docker compose exec backend python manage.py load_ingredients
```

## Примеры:
Запрос: GET: http://127.0.0.1:8000/api/users/
Ответ:
```
{
  "count": 123,
  "next": "http://127.0.0.1:8000/api/users/?page=3",
  "previous": "http://127.0.0.1:8000/api/users/?page=1",
  "results": [
    {
      "email": "user@bb.ru",
      "id": 0,
      "username": "user",
      "first_name": "User",
      "last_name": "User",
      "is_subscribed": false
    }
  ]
}
```

## Документация к API:
```
http://127.0.0.1/api/docs/
```

Автор: [Holorid](https://github.com/Holorid/)