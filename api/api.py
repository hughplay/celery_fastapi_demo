from fastapi import FastAPI
from celery.result import AsyncResult
from worker import celery

app = FastAPI()


@app.post("/add")
async def add_task(x: int, y: int):
    task = celery.send_task("add", args=[x, y], queue="queue_add")
    return {"task_id": task.id}


@app.post("/multiply")
async def multiply_task(x: int, y: int):
    task = celery.send_task("multiply", args=[x, y], queue="queue_multiply")
    return {"task_id": task.id}


@app.get("/check/{task_id}")
async def get_task_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery)
    if task_result.ready():
        return {
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.get(),
        }
    else:
        return {
            "task_id": task_id,
            "status": task_result.status,
            "result": "Not ready",
        }
