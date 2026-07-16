import os
from dotenv import load_dotenv

load_dotenv()

from .schemas import PostBase,PostCreate,PostResponse,User,UserResponse
import psycopg
from typing import Optional
from fastapi import FastAPI,status,HTTPException,Response,Depends
from psycopg.rows import dict_row
import time
from . import models
from sqlalchemy.orm import Session
from .database import engine,get_db
from passlib.context import CryptContext

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
@app.get("/posts",response_model=list[PostResponse])
def get_posts(db: Session=Depends(get_db)):
    # cursor.execute("""Select * From posts """)
    # post=cursor.fetchall()
    post=db.query(models.Post).all()
    return post



#LATEST POST
@app.get('/posts/latest',response_model=PostResponse)
def get_latest_post(db: Session=Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return latest_post

#POST BY ID
@app.get("/posts/{id}",response_model=PostResponse)
def get_posts(id: int,db: Session=Depends(get_db)):
    # cursor.execute("select * from posts where id=%s",(id,))
    # post_by_id=cursor.fetchone()
    post_by_id=db.query(models.Post).filter(models.Post.id==id).first()
    if post_by_id:
        return post_by_id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
   
#CREATE POST
@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=PostResponse)
def create_post(payload: PostCreate,db: Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title,content,is_published) VALUES (%s,%s,%s) RETURNING *""",(payload.title,payload.content,payload.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**payload.model_dump())   
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post 


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
@app.put('/posts/{id}',response_model=PostResponse)
def update_post(id: int, upd_post:PostCreate,db: Session=Depends(get_db)):
    # cursor.execute("""UPDATE POSTS SET title=%s, content=%s, is_published=%s WHERE ID =%s RETURNING *""", (upd_post.title,upd_post.content,upd_post.published,id))
    # new_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
    if post:
        post_query.update(upd_post.model_dump(),synchronize_session=False)
        db.commit()
        db.refresh(post)
        return  post
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found") 

#CreateUsers
@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(payload:User,db: Session=Depends(get_db)):
    user_check=db.query(models.User).filter(models.User.email==payload.email).first()
    if not user_check:
        hashed=pwd_context.hash(payload.password)
        payload.password=hashed
        new_user=models.User(**payload.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="SAME email cant be regitered")
