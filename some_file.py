from celery_2 import add

if __name__ == '__main__':
    result = add.delay(10, 5)
    print(f"Task submitted with ID: {result.id}")

    # Wait for the result and print it
    print(f"Result: {result.get()}")
