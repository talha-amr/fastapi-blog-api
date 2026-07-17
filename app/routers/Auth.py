from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import oauth2
router=APIRouter()
from .. import models
from .. import utils

@router.post('/login')
def login(payload: OAuth2PasswordRequestForm  = Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not utils.pwd_context.verify(payload.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    access_token= oauth2.create_access_token({"user_id": user.id})
    return {"token": access_token, "token-type": "bearer"}

    