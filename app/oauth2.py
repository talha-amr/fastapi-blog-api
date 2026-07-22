from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from . import schemas,database,models
from .config import settings
from jose import JWTError, jwt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
TOKEN_EXPIRATION = settings.token_expiration


def create_access_token(data: dict):
    encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION)
    encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id:str=payload.get("user_id")
        if not user_id:
            raise credentials_exception
        token_data=schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_user(token:str=Depends(oauth2_scheme),db: Session =Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldn't Validate Credentials",headers={"WWW-AUTHENTICATE": "Bearer"})
    token= verify_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()

    if user is None:
        raise credentials_exception

    return user