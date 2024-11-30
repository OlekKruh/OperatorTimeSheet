import json
from datetime import datetime
from sqlalchemy import event, insert
from DataBase.models import ChangeLog, Base
from DataBase.session_manager import get_user_session


def create_log_entry(mapper, connection, target, operation_type, old_values=None, new_values=None):
    table_name = target.__tablename__
    primary_key_column = mapper.primary_key[0].name
    record_id = getattr(target, primary_key_column)

    user_id = get_user_session().get('user_id')

    log_entry = {
        'table_name': table_name,
        'operation_type': operation_type,
        'record_id': record_id,
        'timestamp': datetime.now(),
        'user_id': user_id,
        'old_values': json.dumps(old_values) if old_values else None,
        'new_values': json.dumps(new_values) if new_values else None
    }

    connection.execute(insert(ChangeLog), log_entry)


# Обновляем слушатели
@event.listens_for(Base, 'after_insert')
def after_insert_listener(mapper, connection, target):
    new_values = {column.name: getattr(target, column.name) for column in target.__table__.columns}
    create_log_entry(mapper, connection, target,
                     operation_type='INSERT', new_values=new_values)


@event.listens_for(Base, 'after_update')
def after_update_listener(mapper, connection, target):
    old_values = {column.name: getattr(target, f'_{column.name}_before') for column in target.__table__.columns}
    new_values = {column.name: getattr(target, column.name) for column in target.__table__.columns}
    create_log_entry(mapper, connection, target,
                     operation_type='UPDATE', old_values=old_values, new_values=new_values)


@event.listens_for(Base, 'after_delete')
def after_delete_listener(mapper, connection, target):
    create_log_entry(mapper, connection, target,
                     operation_type='DELETE')


# Регистрация слушателей для всех моделей
def register_listeners():
    for mapper in Base.registry.mappers:
        event.listen(mapper.class_, 'after_insert', after_insert_listener)
        event.listen(mapper.class_, 'after_update', after_update_listener)
        event.listen(mapper.class_, 'after_delete', after_delete_listener)
