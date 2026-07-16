import os
from dotenv import load_dotenv

load_dotenv()

import psycopg
from typing import Optional
from fastapi import FastAPI,status,HTTPException,Response,Depends
from pydantic import BaseModel
import random
from psycopg.rows import dict_row
import time
from . import models
from sqlalchemy.orm import Session
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)
class Post(BaseModel):
    title: str
    content: str
    published: bool = False



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



app = FastAPI()

#ROOT
@app.get("/")
def root():
    return {"message": "Welcome to my API"}

#GET ALL POSTS
@app.get("/posts")
def get_posts(db: Session=Depends(get_db)):
    # cursor.execute("""Select * From posts """)
    # post=cursor.fetchall()
    post=db.query(models.Post).all()
    return {"data": post}



#LATEST POST
@app.get('/posts/latest')
def get_latest_post(db: Session=Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return {"data": latest_post}

#POST BY ID
@app.get("/posts/{id}")
def get_posts(id: int,db: Session=Depends(get_db)):
    # cursor.execute("select * from posts where id=%s",(id,))
    # post_by_id=cursor.fetchone()
    post_by_id=db.query(models.Post).filter(models.Post.id==id).first()
    if post_by_id:
        return {"data": post_by_id}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
   
#CREATE POST
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(payload: Post,db: Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title,content,is_published) VALUES (%s,%s,%s) RETURNING *""",(payload.title,payload.content,payload.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**payload.model_dump())   
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post} 


#DELETE
@app.delete('/posts/{id}')
def delete_post(id: int,db: Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts where id=%s RETURNING *""",(id,))
    # post_by_id=cursor.fetchone()
    # conn.commit()
    post_by_id=db.query(models.Post).filter(models.Post.id==id).first()

    if post_by_id:
        db.delete(post_by_id)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found") 

#UPDATE
@app.put('/posts/{id}')
def update_post(id: int, upd_post:Post,db: Session=Depends(get_db)):
    # cursor.execute("""UPDATE POSTS SET title=%s, content=%s, is_published=%s WHERE ID =%s RETURNING *""", (upd_post.title,upd_post.content,upd_post.published,id))
    # new_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
    if post:
        post_query.update(upd_post.model_dump(),synchronize_session=False)
        db.commit()
        db.refresh(post)
        return {"data": post}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found") 