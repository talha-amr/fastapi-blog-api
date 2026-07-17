from sqlalchemy.orm import Session
from ..schemas import PostCreate,PostResponse
from fastapi import FastAPI,status,HTTPException,Response,Depends,APIRouter
from .. import models
from ..database import get_db

router=APIRouter()
#GET ALL POSTS
@router.get("/posts",response_model=list[PostResponse])
def get_posts(db: Session=Depends(get_db)):
    # cursor.execute("""Select * From posts """)
    # post=cursor.fetchall()
    post=db.query(models.Post).all()
    return post



#LATEST POST
@router.get('/posts/latest',response_model=PostResponse)
def get_latest_post(db: Session=Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return latest_post

#POST BY ID
@router.get("/posts/{id}",response_model=PostResponse)
def get_posts(id: int,db: Session=Depends(get_db)):
    # cursor.execute("select * from posts where id=%s",(id,))
    # post_by_id=cursor.fetchone()
    post_by_id=db.query(models.Post).filter(models.Post.id==id).first()
    if post_by_id:
        return post_by_id
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} not found")
   
#CREATE POST
@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=PostResponse)
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
@router.delete('/posts/{id}')
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
@router.put('/posts/{id}',response_model=PostResponse)
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