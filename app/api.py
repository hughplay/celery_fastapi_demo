from fastapi import FastAPI
from celery.result import AsyncResult
from .celery_worker import app as celery_app

app = FastAPI()


@app.post("/add")
async def add_task(x: int, y: int):
    task = celery_app.send_task("add", args=[x, y])
    return {"task_id": task.id}


@app.post("/multiply")
async def multiply_task(x: int, y: int):
    task = celery_app.send_task("multiply", args=[x, y])
    return {"task_id": task.id}


@app.get("/task/{task_id}/status")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "status": task_result.status}


@app.get("/task/{task_id}/result")
async def get_task_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.ready():
        return {
            "task_id": task_id,
            "status": task_result.status,
            "result": task_result.get(),
        }
    else:
        return {"task_id": task_id, "status": task_result.status, "result": "Not ready"}
