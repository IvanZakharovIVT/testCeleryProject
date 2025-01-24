# Расчет минимальной суммы квадратов для целого числа

## Запуск через докер
```
docker compose up --build -d
```

## Ручной запуск
### Celery
```
celery -A celery_task worker --loglevel=INFO -P threads
```
Для запуска на windows добавить 
``-P threads``
### Fastapi
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
### Redis
```
docker run -d -p 6379:6379 redis 
```

### Запуск воркера
```
schedule_worker.py
```
