from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
import requests
import models
import database

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели Pydantic
class WordBase(BaseModel):
    german: str
    translation: str
    article: str = None
    level: str = "A1"

class WordCreate(WordBase):
    pass

class WordResponse(WordBase):
    id: int
    
    class Config:
        orm_mode = True

class Sentence(BaseModel):
    text: str
    word: str
    correct_form: str

# Зависимость для получения сессии БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    db = database.SessionLocal()
    try:
        # Создаем таблицы, если их нет
        models.Base.metadata.create_all(bind=database.engine)
    finally:
        db.close()

# API для работы со словами
@app.post("/words/", response_model=WordResponse)
def create_word(word: WordCreate, db: Session = Depends(get_db)):
    db_word = models.Word(**word.dict())
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word

@app.get("/words/", response_model=List[WordResponse])
def read_words(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Word).offset(skip).limit(limit).all()

# API для работы с предложениями
@app.get("/sentences/", response_model=List[Sentence])
def get_sentences(word: str):
    try:
        response = requests.get(
            f"https://tatoeba.org/en/api_v0/search?from=deu&to=rus&query={word}",
            timeout=5
        )
        response.raise_for_status()
        
        sentences = []
        for item in response.json().get("results", [])[:5]:  # Берем первые 5 предложений
            sentences.append(Sentence(
                text=item["text"],
                word=word,
                correct_form=word  # TODO: добавить морфологический анализ
            ))
        return sentences
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Сервис примеров предложений временно недоступен"
        )
    
@app.on_event("startup")
def startup():
    # Ждем пока БД станет доступной
    import time
    from sqlalchemy.exc import OperationalError
    
    retries = 5
    while retries > 0:
        try:
            models.Base.metadata.create_all(bind=database.engine)
            break
        except OperationalError:
            retries -= 1
            time.sleep(2)
            if retries == 0:
                raise