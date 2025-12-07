from sqlalchemy import Column, Integer, BigInteger, Boolean, String
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship
Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chats'
    
    id = Column(BigInteger, primary_key=True, autoincrement=False)  # Может быть стоит Integer
    paused = Column(Boolean, default=True, nullable=False)
    # whitelist_entries = relationship("Whitelist", back_populates="chat")


class Whitelist(Base):
    __tablename__ = 'whitelist'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, nullable=False)  # тоже самое про Integer
    username = Column(String(100), nullable=False)  # TO DO: поменять на userId
    # chat = relationship("Chat", back_populates="whitelist_entries")