# Boilerplate-bot

## Описание
***Boilerplate-bot** - телеграм-бот имеющий шаблонный функционал, который может быть кастомизирован под конкретного бота.
Имеет древовидную структуру выдачи информации в виде инлайн-кнопок.
Нажимая на родительскую инлайн-кнопку(узел) получаем список дочерних, которые либо являются узлами, 
либо листьями(узлами, не имеющими дочерних элементов).
Листья содержат медиа-контент(фото, видео, аудио файлы) или текстовую информацию.* <br>

## Технологии:
Python, Django REST Framework, Django MPTT, Aiogram, AIOHTTP, PostgreSQL, docker-compose, Nginx

## Этапы и команды для сборки и запуска приложения:
1. Клонируйте проект в рабочую директорию:<br> 
```git clone https://github.com/annrud/boilerplate-bot.git```
2. Установите <a href="https://docs.docker.com/compose/install/">Docker Compose</a>
3. Создайте образы из корневой папки:<br> 
```docker compose -f infra/docker-compose.local.yaml build```
4. Запустите контейнеры:<br> 
```docker -f infra/docker-compose.local.yaml up -d```
5. Создайте суперпользователя:<br> 
```docker compose -f infra/docker-compose.local.yaml exec bash backend```<br> 
```python manage.py createsuperuser```<br> 

**Проект запустится на http://localhost:80/admin/** <br>

**Дополнительные команды:**<br>
Просмотр запущенных контейнеров:<br>```docker compose -f infra/docker-compose.local.yaml ps```<br>
Остановка и удаление контейнеров:<br>```docker compose -f infra/docker-compose.local.yaml down```<br>
Просмотр логов:<br>```docker compose -f infra/docker-compose.local.yaml logs```<br>
