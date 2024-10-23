import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy_utils import database_exists, create_database as create_new_database
from DataBase.models import Base


def load_db_settings(settings_file='DataBase/db_connection_settings.json'):
    """
    Загрузка настроек подключения к базе данных из указанного файла.
    """
    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
        return settings
    except FileNotFoundError:
        raise Exception('Database settings file not found.')
    except json.JSONDecodeError:
        raise Exception('Error decoding the settings file.')
    except Exception as e:
        raise Exception(f"An error occurred while loading the database settings: {str(e)}")


def get_engine():
    """
    Определяем, существует ли база данных, и подключаемся либо к ней, либо к системной базе.
    """
    db_settings = load_db_settings()

    connection_string = (
        f"postgresql+psycopg2://{db_settings['user']}:{db_settings['password']}"
        f"@{db_settings['host']}:{db_settings['port']}/{db_settings['dbname']}"
    )

    # Проверяем, существует ли база данных
    if database_exists(connection_string):
        # Если база существует, подключаемся к ней
        return create_engine(connection_string)
    else:
        # Если база не существует, подключаемся к системной базе данных (postgres)
        system_connection_string = (
            f"postgresql+psycopg2://{db_settings['user']}:{db_settings['password']}"
            f"@{db_settings['host']}:{db_settings['port']}/postgres"
        )
        return create_engine(system_connection_string)


def get_session(engine):
    """
    Создание сессии с использованием переданного движка.
    """
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except OperationalError as e:
        raise Exception(f'Operational error when creating session: {e}')
    except SQLAlchemyError as e:
        raise Exception(f'General SQLAlchemy error when creating session: {e}')


def get_connection(engine):
    """
    Установка соединения с базой данных.
    """
    try:
        conn = engine.connect()
        return conn
    except OperationalError as e:
        raise Exception(f'Operational error when connecting to database: {e}')
    except SQLAlchemyError as e:
        raise Exception(f'General SQLAlchemy error when connecting to database: {e}')


def create_database():
    """
    Создание базы данных и инициализация таблиц, если база не существует.
    """
    db_settings = load_db_settings()
    engine = get_engine()

    try:
        # Проверяем, существует ли база данных
        if not database_exists(engine.url.set(database=db_settings['dbname'])):
            # Создаём базу данных
            create_new_database(engine.url.set(database=db_settings['dbname']))

            # Подключаемся к новой базе для инициализации таблиц
            engine_new = get_engine()  # Подключаемся к новой базе данных
            Base.metadata.create_all(engine_new)
            return f"Database '{db_settings['dbname']}' created and tables initialized."
        else:
            return f"Database '{db_settings['dbname']}' already exists."
    except OperationalError as e:
        return f"Operational error while creating the database: {e}"
    except SQLAlchemyError as e:
        return f"SQLAlchemy error while creating the database: {e}"
    except Exception as e:
        return f"An error occurred while creating the database: {e}"


def test_db_connection():
    """
    Тестовое подключение к базе данных.
    """
    engine = get_engine()
    try:
        with engine.connect() as conn:
            return "Connection to database successful."
    except OperationalError as e:
        return f"Operational error while connecting to database: {e}"
    except SQLAlchemyError as e:
        return f"SQLAlchemy error while connecting to database: {e}"
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


# def delete_database():
#     db_settings = load_db_settings()
#     engine = get_engine(use_db=False)  # Используем движок без конкретной базы
#
#     try:
#         if database_exists(engine.url):
#             drop_database(engine.url)
#             return f"Database '{db_settings['dbname']}' deleted successfully."
#         else:
#             return f"Database '{db_settings['dbname']}' does not exist."
#     except Exception as e:
#         return f"An error occurred while deleting the database: {e}"
