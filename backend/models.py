from sqlalchemy import Column, Integer, String
from database import Base

class Word(Base):
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True)
    german = Column(String, unique=True, index=True)
    translation = Column(String)
    article = Column(String)  # der, die, das
    level = Column(String)    # A1, A2, B1, etc.