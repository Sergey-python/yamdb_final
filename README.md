![example workflow](https://github.com/Sergey-python/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


## Проект «api_yamdb»

### Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

### Технологии
Python 3.8, Django 2.2, DRF, JWT

<details>
<summary><h3>Как запустить проект</h3></summary>

- Клонировать репозиторий и перейти в директорию для развертывания:

```
git clone git@github.com:Sergey-python/yamdb_final.git
```

```
cd yamdb_final/infra/
```

- Переменные окружения, используемые в проекте(для этого заполните файл .env):

```
DB_ENGINE - указываем, что работаем с postgresql
DB_NAME - имя базы данных
POSTGRES_USER - логин для подключения к базе данных
POSTGRES_PASSWORD - пароль для подключения к БД (установите свой)
DB_HOST - название сервиса (контейнера)
DB_PORT - порт для подключения к БД
```

- Чтобы развернуть проект выполните команду:

```
docker-compose up
```

- Остановка проекта осуществляется нажатием клавиш Ctrl+C.

</details>

### Примеры запросов к API
Примеры запросов доступны в документации по адресу http://127.0.0.1/redoc/ после запуска проекта.

### Проект развернут в облаке
Так же список доступных запросов можно посмотреть по адресу http://pythonman-cloud.ddns.net/redoc/ (http://51.250.66.79/redoc/)
