

Также требуется postgres

```commandline
cp .env.dist .env
docker compose up -d
```

[Схема БД](res/img.png)

Запуск миграций
```commandline
alembic upgrade heads
```

Запуск приложения 
```commandline
uvicorn --factory src.app:create_app
```

При запуске приложения в БД кладутся Пётр и Антон, если их там еще нет.

Запросы
POST /walk_orders

запрос
``` json
{
  "apartment_number": 0,
  "dog_name": "string",
  "dog_breed": "string",
  "walk_date": "2024-08-08",
  "walk_time": "23:39:00.000",
  "walk_duration_in_minutes": 2,
  "walker_name": "Антон" (или Пётр)
}
```

ответ
```json
    id: 1
```

GET /walk_orders?date=2024-08-08

ответ
```json
{
  "walk_orders": [
    {
      "id": 48,
      "apartment_number": 0,
      "dog_name": "string",
      "dog_breed": "string",
      "walk_date": "2024-08-08",
      "walk_time": "23:00:00",
      "walk_duration": 22,
      "walker_id": 3
    },
    {
      "id": 49,
      "apartment_number": 0,
      "dog_name": "string",
      "dog_breed": "string",
      "walk_date": "2024-08-08",
      "walk_time": "23:00:00",
      "walk_duration": 22,
      "walker_id": 2
    }
  ]
}
```


Структура проекта

src/core - слой бизнес логики. Юзкейсы, сервисы, интерфейсы для юзкейсов, сущности.

src/adapters - слой адаптеров. Реализация интерфейсов из core. И еще в sqlalchemy/ лежат миграции алембика.

src/app - слой фреймворка. Зависимости, роуты, создание приложения.

src/app/depends - зависимости. 

src/app/api - роуты.

src/app/create_web_app - создание fastapi приложения.

.

/tests - тесты

Тесты написаны в минимальном количестве только на юзкейсы.