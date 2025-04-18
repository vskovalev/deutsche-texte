import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from time import sleep

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/german_words")

# Добавляем ретраи для подключения
def create_engine_with_retry():
    attempts = 0
    while attempts < 5:
        try:
            return create_engine(DATABASE_URL)
        except Exception as e:
            attempts += 1
            print(f"Connection attempt {attempts} failed, retrying...")
            sleep(2)
    raise Exception("Could not connect to database")

engine = create_engine_with_retry()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()