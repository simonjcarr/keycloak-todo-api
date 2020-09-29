from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import db

app = FastAPI()

origins = [
  "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

#Make values in .env file available
load_dotenv()
cursor = db.get_cursor(db.get_db_connection())

class ToDo(BaseModel):
  task: str
  username: str
  complete: bool

@app.get("/")
def get_user_todos():
  tasks = db.select_query("select * from tasks")
  print(tasks)
  return tasks

@app.post("/")
def create_todo(todo: ToDo):
  sql = f'''
  insert into tasks (task, complete, username)
  values('{todo.task}', '{todo.complete}', '{todo.username}')
  '''
  result = db.execute_sql(sql)
  print("******")
  print(result)
  print("******")
  if (result == 0):
    return "OK"
  else:
    return result

@app.delete("/{task_id}")
def delete_item(task_id: int):
  result = db.execute_sql(f'''delete from tasks where id = {task_id}''')
  if (result == 0):
    return "OK"
  else:
    return result

@app.put("/{task_id}")
def toggle_complete(task_id: int):
  result = db.execute_sql(f'''update tasks set complete = 1 - complete where id = {task_id}''')
  if (result == 0):
    return "OK"
  else:
    return result
