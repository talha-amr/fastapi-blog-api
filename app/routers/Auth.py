from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
router=APIRouter()
from ..schemas import Login
from .. import models
from .. import utils

@router.post('/login')
def login(payload:Login,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==payload.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not utils.pwd_context.verify(payload.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    return {"token": "hellosajnwdoa"}

    