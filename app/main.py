from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post,user,auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True: 
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='postgres',
                                password='password',
                                port="5433",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was SUCCESSFUL!")
        break
    except Exception as error:
            print("Database connection FAILED!")
            print("Error: ",error)  
            time.sleep(2) 
    
my_posts = [{"title":"title of post 1",
             "content":"content of post 1",
             "id":1},
            {"title":"favourite books",
             "content":"I like James Patterson's books",
             "id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
         if p['id'] == id:
             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

          
@app.get("/")
def root():
    return {"message": "Welcome to my API!!"}

