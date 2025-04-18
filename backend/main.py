from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
import requests
import models
import database
from fastapi.responses import HTMLResponse  # Добавьте этот импорт
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
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

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>German Words API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                h1 {
                    color: #2c3e50;
                }
                .links {
                    margin-top: 20px;
                }
                a {
                    display: inline-block;
                    margin-right: 15px;
                    color: #3498db;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1>German Words Learning App - Backend</h1>
            <p>This is the backend API server for the German Words learning application.</p>
            
            <div class="links">
                <a href="/docs">API Documentation (Swagger UI)</a>
                <a href="/redoc">Alternative Docs (ReDoc)</a>
            </div>
            
            <p>Frontend is available at <a href="http://localhost:3000" target="_blank">http://localhost:3000</a></p>
        </body>
    </html>
    """


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
