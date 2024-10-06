import json
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database as create_new_database
from sqlalchemy.orm import sessionmaker
from DataBase.models import Base


def get_engine(db_connection_settings, use_db=True):
    try:
        if use_db:
            connection_string = (
                f"postgresql+psycopg2://{db_connection_settings['user']}:{db_connection_settings['password']}"
                f"@{db_connection_settings['host']}:{db_connection_settings['port']}/{db_connection_settings['dbname']}")
        else:
            connection_string = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"

        engine = create_engine(connection_string)
        return engine
    except SQLAlchemyError as e:
        raise Exception(f'Error connecting to database: {e}')


def get_connection(engine):
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        raise Exception(f'Error connecting to database: {e}')


def create_database(db_connection_settings):
    if not db_connection_settings:
        return 'Database settings are missing!'

    try:
        connection_string = (
            f"postgresql+psycopg2://{db_connection_settings['user']}:{db_connection_settings['password']}"
            f"@{db_connection_settings['host']}:{db_connection_settings['port']}/{db_connection_settings['dbname']}"
        )
        engine = create_engine(connection_string)

        if not database_exists(engine.url):
            create_new_database(engine.url)
            print(f"Database '{db_connection_settings['dbname']}' created.")
        else:
            print(f"Database '{db_connection_settings['dbname']}' already exists.")

        Base.metadata.create_all(engine)

        return f"Database '{db_connection_settings['dbname']}' and tables created successfully!"

    except Exception as e:
        return f"An error occurred: {e}"


def test_db_connection(db_connection_settings):
    if not db_connection_settings:
        return "Database settings are missing."

    try:
        engine = get_engine(db_connection_settings)
        conn = get_connection(engine)
        conn.close()

        return f"Connection to database '{db_connection_settings['dbname']}' successful."
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


def load_db_settings():
    db_connection_settings = 'DataBase/db_connection_settings.json'

    try:
        with open(db_connection_settings, 'r') as f:
            settings = json.load(f)
        return settings
    except FileNotFoundError:
        return 'Database settings file not found.'
    except json.JSONDecodeError:
        return 'Error decoding the settings file.'
    except Exception as e:
        return f"An error occurred while loading the database settings: {str(e)}"
