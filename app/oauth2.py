import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRATION = int(os.getenv("TOKEN_EXPIRATION"))


def create_access_token(data: dict):
    encode = data.copy()

    expire = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION)
    encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt