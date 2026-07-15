import psycopg
from typing import Optional
from fastapi import FastAPI,status,HTTPException,Response
from pydantic import BaseModel
import random
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None

# try:
#     conn=psycopg
# except:
#     pass

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
    return {"data": my_posts}


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
    payload_dict = payload.model_dump()
    payload_dict["id"] = random.randint(1,100000)
    my_posts.append(payload_dict)
    return {"data": payload_dict} 


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