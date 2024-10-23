import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy_utils import database_exists, create_database as create_new_database
from DataBase.models import Base
from contextlib import contextmanager
from DataBase.event_listener import register_listeners


register_listeners()


def load_db_settings(settings_file='DataBase/db_connection_settings.json'):
    """
    Загрузка настроек подключения к базе данных из указанного файла.
    """
    try:
        with open(settings_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise Exception(f"Error loading the settings file: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while loading the database settings: {str(e)}")


def create_connection_string(db_settings, dbname=None):
    """
    Создание строки подключения к базе данных.
    """
    database_name = dbname or db_settings['dbname']
    return (
        f"postgresql+psycopg2://{db_settings['user']}:{db_settings['password']}"
        f"@{db_settings['host']}:{db_settings['port']}/{database_name}"
    )


def get_engine(dbname=None):
    """
    Получение движка базы данных.
    """
    db_settings = load_db_settings()
    connection_string = create_connection_string(db_settings, dbname)
    return create_engine(connection_string)


@contextmanager
def get_db_session():
    """
    Контекстный менеджер для получения сессии базы данных.
    """
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


def get_connection(engine):
    """
    Установка соединения с базой данных.
    """
    try:
        return engine.connect()
    except (OperationalError, SQLAlchemyError) as e:
        raise Exception(f'Error when connecting to the database: {e}')


def create_database():
    """
    Создание базы данных и инициализация таблиц, если база не существует.
    """
    db_settings = load_db_settings()
    engine = get_engine('postgres')  # Подключаемся к системной базе данных

    try:
        # Проверяем, существует ли база данных
        if not database_exists(engine.url.set(database=db_settings['dbname'])):
            # Создаём базу данных
            create_new_database(engine.url.set(database=db_settings['dbname']))

            # Подключаемся к новой базе для инициализации таблиц
            engine_new = get_engine(db_settings['dbname'])
            Base.metadata.create_all(engine_new)
            return f"Database '{db_settings['dbname']}' created and tables initialized."
        else:
            return f"Database '{db_settings['dbname']}' already exists."
    except (OperationalError, SQLAlchemyError) as e:
        return f"Error while creating the database: {e}"
    except Exception as e:
        return f"An unexpected error occurred while creating the database: {e}"


def test_db_connection():
    """
    Тестовое подключение к базе данных.
    """
    engine = get_engine()
    try:
        with get_connection(engine) as conn:
            return "Connection to database successful."
    except (OperationalError, SQLAlchemyError) as e:
        return f"Error while connecting to database: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


def save_db_settings(db_connection_settings):
    """
    Сохранение настроек подключения к базе данных в файл.
    """
    try:
        with open('DataBase/db_connection_settings.json', 'w') as f:
            json.dump(db_connection_settings, f, indent=4)
        return 'Database settings saved successfully.'
    except Exception as e:
        return f'Cannot save Database settings. Error: {e}'
