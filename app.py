from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import pyodbc

app = FastAPI()

class ToDo(BaseModel):
  task: str
  username: str
  complete: bool

@app.get("/")
def get_user_todos():
  return {"Hello": "world"}