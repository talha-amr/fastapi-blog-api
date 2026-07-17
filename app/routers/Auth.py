from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import oauth2

from .. import models
from .. import utils
from .. import schemas
router=APIRouter()
@router.post('/login',response_model=schemas.Token)
def login(payload: OAuth2PasswordRequestForm  = Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==payload.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    verified=utils.pwd_context.verify(payload.password,user.password)
    if not verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    access_token= oauth2.create_access_token({"user_id": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
