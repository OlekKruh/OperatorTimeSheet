from sqlalchemy.orm import Session

from DataBase.event_listener import after_insert_listener


def create_record(session, model, **kwargs):
    """
    Создает новую запись в базе данных. user_id используется только для логирования.
    """
    record = model(**kwargs)  # Создаем запись без user_id
    session.add(record)
    session.flush()  # Промежуточный коммит, чтобы данные были доступны для слушателя

    session.commit()
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
    return record


def delete_record(session: Session, model, filters):
    record = session.query(model).filter_by(**filters).first()
    if record:
        session.delete(record)
        session.commit()
    return record
