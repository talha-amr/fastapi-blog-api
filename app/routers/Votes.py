from fastapi import FastAPI,status,HTTPException,Response,Depends,APIRouter
from ..database import get_db
from .. import oauth2
from sqlalchemy.orm import Session
from ..schemas import Vote
from .. import models



router=APIRouter(prefix='/votes',tags=['Votes'])

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(new_vote:Vote,db: Session= Depends(get_db), current_user= Depends(oauth2.get_user)):
    vote_check=db.query(models.Vote).filter(models.Vote.post_id==new_vote.post_id,models.Vote.user_id==current_user.id).first()
    post_check=db.query(models.Post).filter(models.Post.id==new_vote.post_id).first()
    if not post_check:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cant Find Post")
    if new_vote.dir==1:
        if vote_check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Cant vote Again")
        vote=models.Vote(user_id=current_user.id,post_id=new_vote.post_id)
        db.add(vote)
        db.commit()
        return {"message": "successfully voted"}
    else:
        if not vote_check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="You haven't voted so cant unvote ")
        db.delete(vote_check)
        db.commit()
        return {"message": "successfully removed vote"}