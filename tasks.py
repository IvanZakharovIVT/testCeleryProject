import redis
from celery import Celery

from infrastructure.services.calculate_squares import sum_of_squares

app = Celery('tasks', result_backend ='redis://localhost:6379/0', broker='redis://localhost:6379/0')
app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0'
)

@app.task
def count_square(x: int):
    return sum_of_squares(x)

@app.task
def me_reverse(some_string: str):
    print(f"Task started with input: {some_string}")
    try:
        result = redis.Redis(host='localhost', port=6379, db=0)
        result.set("test_key", "test_value")
        print("Connected to Redis successfully")
        return some_string[::-1]
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        raise
