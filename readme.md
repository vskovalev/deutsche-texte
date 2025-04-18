German Words Learning App
Простое приложение для изучения немецких слов с использованием Docker, FastAPI (бэкенд) и React (фронтенд).

🚀 Быстрый старт
Предварительные требования
Docker (версия 20.10.0+)

Docker Compose (версия 1.29.0+)

Установка и запуск
Клонируйте репозиторий:

bash
Copy
git clone https://github.com/ваш-репозиторий/german-words-app.git
cd german-words-app
Запустите приложение:

bash
Copy
docker-compose up --build
Откройте в браузере:

Фронтенд: http://localhost:3000

Бэкенд (документация API): http://localhost:8000/docs

🛠 Технологический стек
Бэкенд
FastAPI - Python-фреймворк для API

PostgreSQL - реляционная база данных

SQLAlchemy - ORM

Uvicorn - ASGI-сервер

Фронтенд
React - JavaScript-библиотека для UI

React Hooks - управление состоянием

Docker - контейнеризация

Основные функции
Добавление новых слов в словарь

Просмотр списка изученных слов

Примеры предложений с использованием слов

Автоматическая инициализация БД при первом запуске

🛠 Разработка
Запуск в режиме разработки
Запустите только базу данных:

bash
Copy
docker-compose up db
Запустите бэкенд отдельно (из папки backend):

bash
Copy
uvicorn app.main:app --reload
Запустите фронтенд отдельно (из папки frontend):

bash
Copy
npm start
Переменные окружения
Создайте файл .env в корне проекта:

Copy
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=german_words
DATABASE_URL=postgresql://postgres:postgres@db:5432/german_words
🤝 Как помочь проекту
Форкните репозиторий

Создайте ветку (git checkout -b feature/AmazingFeature)

Сделайте коммит (git commit -m 'Add some AmazingFeature')

Запушьте в форк (git push origin feature/AmazingFeature)

Создайте Pull Request

📝 Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE.