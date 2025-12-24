from sqlalchemy import Column, Integer, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Chat(Base):  # type: ignore
    __tablename__ = 'chats'
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    paused = Column(Boolean, default=True, nullable=False)


class Whitelist(Base):  # type: ignore
    __tablename__ = 'whitelist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
