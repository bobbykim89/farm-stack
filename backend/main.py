from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import Todo

# App object
app = FastAPI()

from database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo
)

origins = ['https://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get(('/'))
def read_root():
    return {'Message': 'Hello World!'}

@app.get('/api/todo')
async def get_todo():
    res = await fetch_all_todos()
    return res

@app.get('/api/todo{title}', response_model=Todo)
async def get_todo_by_id(title):
    res = await fetch_one_todo(title)
    if res:
        return res
    raise HTTPException(404, f'There is no TODO item with this title {title}')

@app.post('/api/todo', response_model=Todo)
async def post_todo(todo: Todo):
    res = await create_todo(todo.dict())
    if res:
        return res
    raise HTTPException(400, "Something went wrong / Bad request")

@app.put('/api/todo{title}', response_model=Todo)
async def put_todo(title: str, desc: str):
    res = await update_todo(title, desc)
    if res:
        return res
    raise HTTPException(404, f'There is no TODO item with this title {title}')

@app.delete('/api/todo{title}')
async def delete_todo(title):
    res = await remove_todo(title)
    if res:
        return 'Successfully deleted todo item!'
    raise HTTPException(404, f'There is no TODO item with this title {title}')