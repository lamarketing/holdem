# Сайт для игры в техасский холдем
#### онлайн фриролл турнир каждый день
Расчетная готовность MVP - середина мая 2022

Технологии:
1. Django 4.0, DRF
2. Django-Channels, ASGI, Redis
3. Celery, Redis, Django-Celery-Beat
4. Vue.js 3.2
5. Postgresql 14
6. Docker


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
Для Table  сделать bb
Если check:
...

Обработка максимального стека
Из raise вычитать (how_many_rows + 1) * init_bb
И raise, и all-in не может быть больше
самого большого стека среди всех игроков.
Если самый большой стек принадлежит игроку,
то надо искать второй больший стек.
Значит, берем на клиенте все стеки игроков,
кроме себя, и без fold, и находим больший.
На сервере тоже делаем проверку.

Если all-in сразу больше чьего-то максимального стека,
то all-in неактивен.

Если all-in раньше больше стека настоящего игрока,
то нужно в Player добавить поля bet и is_all_in

Тогда 2-ой pot делать не нужно.

bb = 10, next_bb = 20
1-5  30  Fold либо +5(call), либо all-in 
2-10 30  Fold
3-50 150 Raise!
4-20 20  All-in мог идти только  all-in
5-10 10  All-in (winner)
6-0 Fold(s=200, max=100)

Pot=95

PW = 5 + 10 + 10 + 10 + 10 = 45

bb = 10, next_bb = 20
1-5  30(25) (AF)
2-10 25(15)  (AF)
3-50  150 to_call=10 r=130 all-in=150 (CRAF)
4-20 20  (AF)
5-10 10  (A)
6-0  200 to_call=50, r=100, all_in=! (CRF)

if to_call:
Если стек <= to_call -> (A -CRF)
Если стек <= next_bb -> (A -CRF)
else:
mr = stack - nex_bb 110 - 20 = 90
is_mr = mr <= max stack (Bool)
if is_mr -> (+R)
else -> mr = max stack (+R -A)

Когда (A) не позволен:


Если mr <







