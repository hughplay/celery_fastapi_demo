from celery import shared_task


@shared_task(name="add")
def add(x, y):
    return x + y


@shared_task(name="multiply")
def multiply(x, y):
    return x * y
