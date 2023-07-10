from fastapi import FastAPI #PIP install fastapi
from pydantic import BaseModel #PIP install pydantic
import json

app = FastAPI()

class Group(BaseModel):
    name: str

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/get_students/{group_name}')
def get_students(group_name: str):
    with open('students.json', 'r') as f:
        groups = json.load(f)
    for g in groups:
        if g['group'] == group_name:
            return {"students": g['students']}
    return {"students": []}
