import os
from datetime import datetime, timedelta, timezone
from . import schemas
from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRATION = int(os.getenv("TOKEN_EXPIRATION"))


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
    
def get_user(token:str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldn't Validate Credentials",headers={"WWW-AUTHENTICATE": "Bearer"})
     
    return verify_token(token,credentials_exception)