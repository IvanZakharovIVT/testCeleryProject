from celery import Celery

# Create a Celery app instance
app = Celery('tasks', broker='redis://localhost:6379/0',
             result_backend='redis://localhost:6379/0')


@app.task
def add(x, y):
    """A simple task that adds two numbers."""
    result = x + y
    return result


if __name__ == '__main__':
    # Test the task
    result = add.delay(4, 4)
    print(f"Task submitted with ID: {result.id}")

    # Wait for the result and print it
    print(f"Result: {result.get()}")