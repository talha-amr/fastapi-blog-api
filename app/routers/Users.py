from ..schemas import User,UserResponse
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,utils
from fastapi import FastAPI,status,HTTPException,Response,Depends,APIRouter


router=APIRouter(prefix='/users',tags=['User'])


#CreateUsers
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(payload:User,db: Session=Depends(get_db)):
    user_check=db.query(models.User).filter(models.User.email==payload.email).first()
    if not user_check:
        payload.password=utils.hashed(payload.password)
        new_user=models.User(**payload.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="SAME email cant be regitered")



#GET ALL USERS
@router.get('/',response_model=list[UserResponse])
def getUsers(db: Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users

#GET USER BY ID
@router.get('/{id}',response_model=UserResponse)
def get_user_by_id(id:int,db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID not Found")
    return user
