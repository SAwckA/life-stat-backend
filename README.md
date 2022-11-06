## Api server для приложения LifeStat

<hr>

### Основые функиции:

* Запросы к базе данных 
* Аутентификация/авторизация пользователя посредством :Warning: **только Access JWT** (сессии не сохраняются, токен валиден 30 дней)
* Является полностью **stateless** 

### Внешние зависимости
* Основная база данных: **PostgresQL** 
* Тестовая база данных: **SQLite3** :Warning: *Это может нести некоторые последствия, хоть и интерфейсы адаптированы*
* По факту приложение работает совершенно независимо по своей принадлежности

<hr>

### Запуск собранного приложения

> Команда для запуска приложения в докер + автоматическое обновление до версии latest
```bash
# Загрузка репозитория не требуется 

docker run -d --rm --name api \
  -p "8000:8000" \
  -e DB_ENV=DEV -e \
  SECRET_KEY=asdqwezxc \
  ghcr.io/sawcka/life-stat-backend:release &&
docker run -d \
  --rm --name watchtower \
  -v $HOME/.docker/config.json:/config.json \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower api --debug
```
> Документация к API станет доступна по адресу **0.0.0.0/docs**
<hr>

### Запуск исходного кода:

> Установка коружения

```shell
$ python3 -m venv venv
```
```shell
$ . venv/bin/activate 
```

```shell
$ pip install -r requirements.txt
```
> Запуск проекта

```shell
$ make run
```
> Документация к API станет доступна по адресу **0.0.0.0/docs**

<hr>

### Для тестировки/отладки используются следующие sql файлы:

> Инициализация структуры базы данных 

* init_test.sql 

> Тестовые данные

* data_test.sql

> :Warning: Тестовая база данных (**sqlite3**) создаётся в **оперативной памяти** и хранит своё состояние только на протяжении работы приложения. При повтором запуске приложения, база данных **заново инициализируется** в памяти из этих файлов 

