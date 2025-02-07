from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    birthdate = Column(String, nullable=False)
    
    library = relationship("Library", back_populates='users')
    
class Library(Base):
    __tablename__ = 'libraries'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="library")
    games = relationship("Game", back_populates="library")
    
class Game(Base):
    __tablename__ = 'games'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    search_result = Column(Text)
    rating = Column(Integer)
    state = Column(String)  # "played", "not played", "wishlisted", etc.
    library_id = Column(Integer, ForeignKey("libraries.id"))
    
    library = relationship("Library", back_populates="games")
