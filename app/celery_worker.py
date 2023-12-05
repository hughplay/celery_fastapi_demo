from celery import Celery

app = Celery(
    __name__,
    backend="rpc://",  # You can change the backend as per your requirement
    broker="pyamqp://guest:guest@localhost:5672//",  # URL for RabbitMQ, change as needed
    include=["services.simple_tasks"],  # List of modules to import when the Celery worker starts
)
