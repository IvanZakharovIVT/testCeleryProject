from celery import Celery, Task
from infrastructure.services.calculate_squares import sum_of_squares

class PageTask(Task):
    name = 'page_task'

    def run(self, n_value: int):
        print("start task")
        r = sum_of_squares(n_value)
        print(r)
        return r


app = Celery('celery_task', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app.conf.broker_url = 'redis://localhost:6379/0'
app.register_task(PageTask())

@app.task
def add_new_task(n_value):
    print("start task")
    r = sum_of_squares(n_value)
    print(r)
    return r
