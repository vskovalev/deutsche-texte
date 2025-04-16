Хорошо! Создадим прототип приложения для изучения немецких слов с использованием Docker. Это позволит легко развернуть локальную среду разработки или даже выложить приложение в продакшен.

Структура проекта
Copy
/
├── backend/               # FastAPI-сервер (бэкенд)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
├── frontend/              # React-приложение (фронтенд)
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── docker-compose.yml      # Объединяет сервисы
└── .env                    # Переменные окружения (опционально)
1. Backend (FastAPI)
Функции:

Хранение слов (CRUD).

Запросы к внешнему API (например, Tatoeba) для поиска примеров предложений.

Файлы
backend/Dockerfile
dockerfile
Copy
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
backend/requirements.txt
Copy
fastapi>=0.68.0
uvicorn>=0.15.0
requests>=2.26.0
pydantic>=1.8.0
sqlalchemy>=1.4.0
backend/main.py
python
Copy
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

# Модели данных
class Word(BaseModel):
    id: int
    german: str
    translation: str

class Sentence(BaseModel):
    text: str
    word: str  # слово из словаря (в начальной форме)
    correct_form: str  # слово в форме из предложения

# "База данных" (временная, для прототипа)
words_db = []
sentences_db = []

# API для работы со словарём
@app.post("/words/", response_model=Word)
def add_word(word: Word):
    words_db.append(word)
    return word

@app.get("/words/", response_model=List[Word])
def get_words():
    return words_db

# API для заданий (предложений)
@app.get("/sentences/", response_model=List[Sentence])
def get_sentences(word: str):
    # Запрос к Tatoeba API (пример)
    response = requests.get(f"https://tatoeba.org/en/api_v0/search?from=deu&query={word}")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Предложения не найдены")
    
    sentences = []
    for item in response.json()["results"]:
        sentences.append(Sentence(
            text=item["text"],
            word=word,
            correct_form=word  # TODO: морфологический анализ
        ))
    
    return sentences
2. Frontend (React)
Файлы
frontend/Dockerfile
dockerfile
Copy
FROM node:16-alpine

WORKDIR /app
COPY package.json .
RUN npm install

COPY . .

CMD ["npm", "start"]
frontend/src/App.js (упрощённый вариант)
jsx
Copy
import React, { useState, useEffect } from 'react';

function App() {
  const [words, setWords] = useState([]);
  const [newWord, setNewWord] = useState({ german: '', translation: '' });

  // Загрузка слов с бэкенда
  useEffect(() => {
    fetch('http://backend:8000/words')
      .then(res => res.json())
      .then(data => setWords(data));
  }, []);

  const addWord = () => {
    fetch('http://backend:8000/words', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newWord)
    }).then(() => {
      setWords([...words, newWord]);
      setNewWord({ german: '', translation: '' });
    });
  };

  return (
    <div>
      <h1>Немецкий словарь</h1>
      <div>
        <input
          value={newWord.german}
          onChange={(e) => setNewWord({ ...newWord, german: e.target.value })}
          placeholder="Немецкое слово"
        />
        <input
          value={newWord.translation}
          onChange={(e) => setNewWord({ ...newWord, translation: e.target.value })}
          placeholder="Перевод"
        />
        <button onClick={addWord}>Добавить</button>
      </div>
      <ul>
        {words.map((word, idx) => (
          <li key={idx}>{word.german} - {word.translation}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
3. Docker Compose
docker-compose.yml
yaml
Copy
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped
4. Запуск
Убедитесь, что у вас установлены Docker и Docker Compose.

В корне проекта выполните:

bash
Copy
docker-compose up --build
Откройте в браузере:

Фронтенд: http://localhost:3000

Бэкенд (API): http://localhost:8000/docs (Swagger)

Что можно улучшить
✅ База данных → Заменить временный список на PostgreSQL.
✅ Авторизация → Добавить JWT-аутентификацию.
✅ Тесты → Написать unit-тесты для бэкенда.
✅ Морфологический анализ → Использовать библиотеку spaCy (для определения формы слова в предложении).

