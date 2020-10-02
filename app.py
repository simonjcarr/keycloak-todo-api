from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import db
import security

app = FastAPI()

origins = [
  "*",
  "http://192.168.30.100:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

cursor = db.get_cursor(db.get_db_connection())

class ToDo(BaseModel):
  task: str
  complete: bool

@app.get("/")
def get_user_todos(request: Request):
  user = security.get_user(request)
  if not user:
    raise HTTPException(status_code=403, detail="Unable to find your username.")
  tasks = db.select_query(f"select * from tasks where username = '{user['username']}'")
  return tasks

@app.post("/")
def create_todo(request: Request, todo: ToDo):
  if not security.user_has_role(request, "CREATE_TODO"):
    raise HTTPException(
        status_code=403, detail="You don't have permission to create ToDo's")
  user = security.get_user(request)
  sql = f'''
  insert into tasks (task, complete, username)
  values('{todo.task}', '{todo.complete}', '{user["username"]}')
  '''
  result = db.execute_sql(sql)
  if (result == 0):
    return "OK"
  else:
    return result

@app.delete("/{task_id}")
def delete_item(request: Request, task_id: int):
  if not security.user_has_role(request, "DELETE_TODO"):
    raise HTTPException(
        status_code=403, detail="You don't have permission to delete ToDo's")
  result = db.execute_sql(f'''delete from tasks where id = {task_id}''')
  if (result == 0):
    return "OK"
  else:
    return result

@app.put("/{task_id}")
def toggle_complete(request: Request, task_id: int):
  if not security.user_has_role(request, "TOGGLE_TODO"):
    raise HTTPException(
        status_code=403, detail="You don't have permission to Toggle ToDo's")
  result = db.execute_sql(f'''update tasks set complete = 1 - complete where id = {task_id}''')
  if (result == 0):
    return "OK"
  else:
    return result
