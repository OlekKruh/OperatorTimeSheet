from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
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


def check_database(host, port, user, password, dbname):
    return f'in progress'


def create_database(host, port, user, password, dbname):
    return f'in progress'


def test_db_connection(host, port, user, password, dbname):
    return f'in progress'


def save_db_settings(host, port, user, password, dbname):
    try:
        settings = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'dbname': dbname
        }
        with open('DataBase/db_connection_settings.json', 'w') as f:
            json.dump(settings, f, indent=4)
        return f'Database settings saved successfully.'

    except Exception as e:
        return f'Cannot save Database settings. Error: {str(e)}'


def load_db_settings():
    settings_file = 'DataBase/db_connection_settings.json'

    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
        return settings
    except Exception as e:
        return None
