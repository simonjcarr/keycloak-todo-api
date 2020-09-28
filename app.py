from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_user_todos():
  return {"Hello": "world"}