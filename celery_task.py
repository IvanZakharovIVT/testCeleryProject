from celery import Celery

from src.config.settings import MAX_TASK_EXECUTION_TIME, REDIS_PATH
from src.infrastructure.services.calculate_squares import sum_of_squares


app = Celery('celery_task', result_backend =REDIS_PATH, broker=REDIS_PATH)
app.conf.update(
    broker_url=REDIS_PATH,
    result_backend=REDIS_PATH
)

@app.task(time_limit=MAX_TASK_EXECUTION_TIME)
def add_new_task(n_value: int) -> str:
    print("start task")
    r = sum_of_squares(n_value)
    print(r)
    return r.model_dump_json()
