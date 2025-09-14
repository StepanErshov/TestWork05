# Quotes Scraper Service

Сервис для парсинга цитат с сайта quotes.toscrape.com и предоставления доступа к ним через API.

## Функциональность

- **POST /parse-quotes-task** - запуск задачи парсинга цитат
- **GET /quotes** - получение цитат с фильтрацией по автору и/или тегу
- Асинхронная обработка с использованием Celery + Redis
- Хранение данных в MongoDB

## Запуск проекта

### Требования

- Docker
- Docker Compose

### Инструкция по запуску

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd quotes_scraper
```
2. Соберите и запустите контейнеры:
```bash
docker-compose up --build
```
3. Сервис будет доступен по адресу: http://localhost:8000

4. Документация API доступна по адресу: http://localhost:8000/docs

## Использование API

### Запуск парсинга

```bash
curl -X POST http://localhost:8000/parse-quotes-task
```

Ответ:
```json
{
  "task_id": "task-uuid"
}
```

### Получение цитат

```bash
# Все цитаты
curl http://localhost:8000/quotes

# Фильтр по автору
curl http://localhost:8000/quotes?author=Albert

# Фильтр по тегу
curl http://localhost:8000/quotes?tag=life

# Комбинированный фильтр
curl http://localhost:8000/quotes?author=Albert&tag=life
```

### Структура сервисов
- web: FastAPI приложение (порт 8000)

- celery_worker: Celery воркер для фоновых задач

- redis: Брокер сообщений для Celery (порт 6379)

- mongo: База данных MongoDB (порт 27017)

### Технологии
- FastAPI - веб-фреймворк

- Celery - распределенная очередь задач

- Redis - брокер сообщений

- MongoDB - база данных

- BeautifulSoup4 - парсинг HTML

- Docker & Docker Compose - контейнеризация

## Запуск проекта

1. Создайте все файлы в соответствующей структуре папок
2. Запустите команду:
```bash
docker-compose up --build
```
3. Откройте браузер и перейдите по адресу http://localhost:8000/docs для доступа к документации API