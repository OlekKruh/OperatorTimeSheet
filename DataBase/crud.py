from sqlalchemy.orm import Session
from .cache_manager import add_to_cache, update_cache, delete_from_cache, get_cache


def get_records(tab_name):
    """Получает записи из кеша для указанной таблицы."""
    return get_cache(tab_name)


def create_record(session, model, **kwargs):
    """Создает новую запись в базе данных."""
    record = model(**kwargs)  # Создаем запись без user_id
    session.add(record)
    session.flush()  # Промежуточный коммит, чтобы данные были доступны для слушателя
    session.commit()
    add_to_cache(model.__tablename__, record)
    return record


def read_records(session: Session, model, filters=None):
    query = session.query(model)
    if filters:
        query = query.filter_by(**filters)
    return query.all()


def update_record(session: Session, model, filters, update_data):
    record = session.query(model).filter_by(**filters).first()
    if record:
        for key, value in update_data.items():
            setattr(record, key, value)
        session.commit()
        update_cache(model.__tablename__, record.id, record)
    return record


def delete_record(session: Session, model, filters):
    record = session.query(model).filter_by(**filters).first()
    if record:
        session.delete(record)
        session.commit()
        delete_from_cache(model.__tablename__, record.id)
    return record
