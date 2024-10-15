from sqlalchemy.orm import Session


def create_record(session: Session, model, **kwargs):
    record = model(**kwargs)
    session.add(record)
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
