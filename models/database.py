from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание базы данных (замените строку подключения на вашу)
DATABASE_URL = 'sqlite:///..//data/test.db'  # Пример для SQLite
#
# DATABASE_URL = 'sqlite://data/test.db'
engine = create_engine(DATABASE_URL)

# Создание базового класса для моделей
Base = declarative_base()
# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

