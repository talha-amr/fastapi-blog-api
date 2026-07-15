import os
from dotenv import load_dotenv

load_dotenv()

import psycopg
from typing import Optional
from fastapi import FastAPI,status,HTTPException,Response
from pydantic import BaseModel
import random
from psycopg.rows import dict_row
import time

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
connection=False
while not connection:
    try:
        conn = psycopg.connect(
            host=os.getenv("DATABASE_HOSTNAME"),
            dbname=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USERNAME"),
            password=os.getenv("DATABASE_PASSWORD"),
            port=os.getenv("DATABASE_PORT"),
            row_factory=dict_row,
        )

        cursor = conn.cursor()
        print("Database connection successful")
        connection=True
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(3)


my_posts = [
    {
        "title": "Getting Started with FastAPI",
        "content": "FastAPI is a modern Python framework for building APIs quickly and efficiently.",
        "published": True,
        "rating": 4.8,
        "id": 1
    },
    {
        "title": "Understanding Python Dictionaries",
        "content": "Dictionaries store data as key-value pairs and provide fast lookups.",
        "published": False,
        "rating": 4.5,
        "id": 2
    },
    {
        "title": "Why Learn Backend Development?",
        "content": "Backend development allows you to build APIs, manage databases, and handle business logic.",
        "published": True,
        "rating": 4.9,
        "id": 3
    }
]
app = FastAPI()

#ROOT
@app.get("/")
def root():
    return {"message": "Welcome to my API"}

#GET ALL POSTS
@app.get("/posts")
def get_posts():
    cursor.execute("""Select * From posts """)
    post=cursor.fetchall()
    return {"data": post}


#LATEST POST
@app.get('/posts/latest')
def get_latest_post():
    latest_post = my_posts[-1]
    return {"data": latest_post}

#POST BY ID
@app.get("/posts/{id}")
def get_posts(id: int):
    for post in my_posts:
        if post["id"] == id:
            return {"data": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
   
#CREATE POST
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    cursor.execute("""INSERT INTO posts(title,content,is_published) VALUES (%s,%s,%s) RETURNING *""",(payload.title,payload.content,payload.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data": new_post} 


#DELETE
@app.delete('/posts/{id}')
def delete_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            my_posts.remove(post)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found") 

#UPDATE
@app.put('/posts/{id}')
def update_post(id: int, upd_post:Post):
    for post in my_posts:
        if post['id'] == id:
            post.update(upd_post.model_dump())
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found") 