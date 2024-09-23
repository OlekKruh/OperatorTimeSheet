from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/kradex_ploter_db')


def get_engine():
    """
    Создаем движок базы данных. Если база данных не существует, она будет создана автоматически.
    """
    if not os.path.exists('./database.db'):
        print("База данных не найдена, создаем новую...")

    engine = create_engine(DATABASE_URL, echo=True)  # echo=True для вывода SQL-запросов в консоль
    return engine


def create_session(engine):
    """
    Создаем сессию для взаимодействия с базой данных.
    """
    Session = sessionmaker(bind=engine)
    return Session()


def init_db(engine, Base):
    """
    Инициализируем базу данных, создавая таблицы.
    """
    Base.metadata.create_all(engine)
    print("Таблицы успешно созданы.")


def check_database():
    return f'in progress'

