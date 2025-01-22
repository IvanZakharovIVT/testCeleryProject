from celery import Celery

from config.settings import MAX_TASK_EXECUTION_TIME
from infrastructure.services.calculate_squares import sum_of_squares


app = Celery('celery_task', result_backend ='redis://localhost:6379/0', broker='redis://localhost:6379/0')
app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0'
)

@app.task(time_limit=MAX_TASK_EXECUTION_TIME)
def add_new_task(n_value: int) -> str:
    print("start task")
    r = sum_of_squares(n_value)
    print(r)
    return r.model_dump_json()
