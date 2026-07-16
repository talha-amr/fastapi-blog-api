from .database import Base
from sqlalchemy import String,Integer,Boolean,Column,TIMESTAMP
from sqlalchemy.sql import text
class Post(Base):
    __tablename__="posts"
    id= Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content= Column(String,nullable=False)
    published=Column(Boolean,server_default="False") 
    created_at= Column(TIMESTAMP(timezone="True"),server_default=text('NOW()'))