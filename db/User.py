from sqlalchemy import Column, VARCHAR,Integer, DATE, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from .base import BaseModel
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy_json import mutable_json_type

class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(Integer, unique = True, nullable=False, primary_key=True)
    
    telegram_user_id = Column(BigInteger, unique = True, nullable=False,)

    bot_language = Column(VARCHAR(32), unique=False, default='eng')
    
    translation_language = Column(VARCHAR(32), unique=False, default='eng')

    dictionary = Column(mutable_json_type(dbtype=JSONB, nested=True), default={})

    training_mode_state = Column(mutable_json_type(dbtype=JSONB, nested=True), default={})

    def __str__(self) -> str:
        return f'<User:{self.user_id}>'