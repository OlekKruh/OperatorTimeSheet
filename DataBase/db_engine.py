import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database as create_new_database
from DataBase.models import Base


def load_db_settings():
    try:
        with open('DataBase/db_connection_settings.json', 'r') as f:
            settings = json.load(f)
        return settings
    except FileNotFoundError:
        raise Exception('Database settings file not found.')
    except json.JSONDecodeError:
        raise Exception('Error decoding the settings file.')
    except Exception as e:
        raise Exception(f"An error occurred while loading the database settings: {str(e)}")


def get_engine(use_db=True):
    db_settings = load_db_settings()  # Загружаем настройки из файла
    try:
        if use_db:
            connection_string = (
                f"postgresql+psycopg2://{db_settings['user']}:{db_settings['password']}"
                f"@{db_settings['host']}:{db_settings['port']}/{db_settings['dbname']}")
        else:
            connection_string = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"

        engine = create_engine(connection_string)
        return engine
    except SQLAlchemyError as e:
        raise Exception(f'Error connecting to database: {e}')


def get_session(engine):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except SQLAlchemyError as e:
        raise Exception(f'Error creating session: {e}')


def get_connection(engine):
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        raise Exception(f'Error connecting to database: {e}')


def create_database():
    db_settings = load_db_settings()
    engine = get_engine(use_db=False)

    try:
        if not database_exists(engine.url):
            create_new_database(engine.url)
            Base.metadata.create_all(engine)
            return f"Database '{db_settings['dbname']}' created and tables initialized."
        else:
            return f"Database '{db_settings['dbname']}' already exists. No action taken."
    except Exception as e:
        return f"An error occurred: {e}"


def test_db_connection():
    engine = get_engine()
    try:
        conn = engine.connect()
        conn.close()
        return f"Connection to database successful."
    except SQLAlchemyError as e:
        return f"Error connecting to database: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


def save_db_settings(db_connection_settings):
    try:
        with open('DataBase/db_connection_settings.json', 'w') as f:
            json.dump(db_connection_settings, f, indent=4)
        return f'Database settings saved successfully.'

    except Exception as e:
        return f'Cannot save Database settings. Error: {str(e)}'
