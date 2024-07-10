from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4


app = FastAPI()

# Pydantic Model
class Task(BaseModel):
    id: Optional[UUID] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = False

# In-Memory database
tasks = []

# create a task
@app.post("/create-task", response_model=Task)
def create_task(task: Task):
    task.id = uuid4()
    tasks.append(task)
    
    return task

# get all tasks
@app.get("/get-tasks/", response_model=List[Task])
def get_tasks():
    return tasks

# get task by id
@app.get("/get-task/{task_id}", response_model=Task)
def get_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task
    
    raise HTTPException(status_code=404, detail="Task not found")

# update task by id
@app.put("/update-task/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = task.copy(update=task_update.dict(exclude_unset=True))
            tasks[index] = updated_task
            
            return tasks[index]
    raise HTTPException(status_code=404, detail="Task not found") 

# delete task by id
@app.delete("/delete-task/{task_id}", response_model=Task)
def delete_task(task_id: UUID):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(index)   
    
    raise HTTPException(status_code=404, detail="Task not found")
    

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3000)