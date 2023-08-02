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

## Запуск проекта
1. Клонирование репозитория
```
git clone git@github.com:Holorid/foodgram-project-react.git
```

Откройте терминал проекта, клонированного ранее

2. Развертывание в репозитории виртуального окружения
```
Windows:
python -m venv venv

MacOS/Linux:
python3 -m venv venv
```
3. Запуск виртуального окружения
```
Windows:
source venv/Scripts/activate

MacOS/Linux:
source venv/bin/activate

```
4. Установка зависимостей в виртуальном окружении
```
pip install -r requirements.txt
```

5. Выполнение миграций
```
python manage.py migrate
```

6. Запуск проекта
```
python manage.py runserver
```

7. Установка зависимости для фронтенд-приложения
```
cd ./frontend/
npm i
```