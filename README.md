# Сайт для игры в техасский холдем
#### онлайн фриролл турнир каждый день
Расчетная готовность MVP - середина мая 2022

Технологии:
1. Django 4.0, DRF
2. Django-Channels как ASGI + Redis
3. Vue.js 3.0
4. Postgresql 14
5. Docker


## HOW INSTALL
Важно!!!
Поскольку используется AbstractUser, у которого изменен id на uuid,
то _**abstractuser**_ нужно мигрировать строго до первого migrate

```
$ python manage.py makemigrations abstractuser
$ python manage.py migrate
```

Потом надо добавить в БД карты
```
$ python manage.py makemigrations cards
$ python manage.py migrate
$ python manage.py create_cards
```