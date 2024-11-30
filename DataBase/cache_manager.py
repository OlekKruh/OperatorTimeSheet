import asyncio
from datetime import datetime
from DataBase.db_engine import get_db_session
from DataBase.models import model_mapping, ChangeLog

_cache_data = {}
_last_checked = datetime.now()
cache_update_event = asyncio.Event()


def initialize_cache():
    """Инициализирует кеш данными из БД при запуске."""
    with get_db_session() as session:
        for tab_name, model in model_mapping.items():
            # Загружаем все записи из базы данных и сохраняем в кеш
            _cache_data[tab_name] = session.query(model).all()
            print(f"Table '{tab_name}' cache initialized with {_cache_data[tab_name]} records.\n")

        # Получаем последний timestamp из таблицы ChangeLog
        _last_checked_entry = session.query(ChangeLog).order_by(ChangeLog.timestamp.desc()).first()
        global _last_checked
        if _last_checked_entry:
            _last_checked = _last_checked_entry.timestamp
            print(f"Last timestamp in ChangeLog is: {_last_checked}\n")
        else:
            _last_checked = datetime.now()  # Если нет записей в ChangeLog, используем текущее время
            print("No entries in ChangeLog. Using current time as last checked timestamp.\n")


def get_data_from_cache(tab_name):
    """Возвращает данные из кеша для модели."""
    data = _cache_data.get(tab_name, [])
    print(f"Data retrieved from cache for '{tab_name}': {data} records found.\n")
    return data


def update_cache_from_changelog():
    """Обновляет кеш на основе последних 100 записей из ChangeLog."""
    global _last_checked
    with get_db_session() as session:
        # Получаем последние 100 записей из ChangeLog, сортируя по времени создания
        recent_changes = session.query(ChangeLog) \
            .order_by(ChangeLog.timestamp.desc()) \
            .limit(50) \
            .all()

        # Фильтруем записи, которые были созданы позже _last_checked
        new_changes = [entry for entry in recent_changes if entry.timestamp > _last_checked]

        if not new_changes:
            print("No new entries found in ChangeLog to update cache.\n")
            return

        for entry in new_changes:
            tab_name = entry.table_name
            record_id = entry.record_id
            operation_type = entry.operation_type

            if tab_name not in model_mapping:
                print(f"Table '{tab_name}' not found in model mapping. Skipping...\n")
                continue

            model = model_mapping[tab_name]

            primary_key_map = {
                'users': 'user_id',
                'operator': 'operator_id',
                'company': 'company_id',
                'enclosure': 'enclosure_id',
                'machine': 'machine_id',
                'order': 'order_id',
                'time_sheet': 'row_id'
            }

            match operation_type:
                case 'INSERT':
                    # Добавляем новую запись в кеш
                    new_record = session.query(model).get(record_id)
                    if new_record:
                        if tab_name in _cache_data:
                            _cache_data[tab_name].append(new_record)
                        else:
                            _cache_data[tab_name] = [new_record]
                        print(f"Record with ID '{record_id}' added to cache for table '{tab_name}'.\n")

                case 'UPDATE':
                    # Обновляем запись в кеше, заменяя старую версию на новую
                    updated_record = session.query(model).get(record_id)
                    if updated_record:
                        primary_key = primary_key_map.get(tab_name, 'id')

                        _cache_data[tab_name] = [
                            record if getattr(record, primary_key) != record_id else updated_record
                            for record in _cache_data[tab_name]
                        ]
                        print(f"Record with ID '{record_id}' updated in cache for table '{tab_name}'.\n")

                case 'DELETE':
                    # Удаляем запись из кеша по record_id
                    primary_key = primary_key_map.get(tab_name, 'id')

                    _cache_data[tab_name] = [
                        record for record in _cache_data[tab_name] if getattr(record, primary_key) != record_id
                    ]
                    print(f"Record with ID '{record_id}' deleted from cache for table '{tab_name}'.\n")

        # Обновляем _last_checked до времени последней обработанной записи
        _last_checked = max(entry.timestamp for entry in new_changes)
        print(f"Cache successfully updated up to {_last_checked}.\n")


async def async_poll_change_log():
    """Опрос таблицы ChangeLog каждые 60 секунд на предмет изменений."""
    global cache_update_event
    while True:
        await cache_update_event.wait()  # Ждем пока истечет время, или произойдет принудительное обновление кеша
        update_cache_from_changelog()  # Обновляем кеш из ChangeLog

        cache_update_event.clear()  # После обновления сбрасываем событие и начинаем отсчет заново

        await asyncio.sleep(60)  # Ждем 60 секунд перед следующим обновлением
        cache_update_event.set()  # Устанавливаем событие, чтобы позволить обновление кеша (если никто не вмешается)


def crud_update_cache():
    """Принудительно обновляет кеш и сбрасывает таймер опроса."""
    try:
        update_cache_from_changelog()
    except Exception as error:
        print(f"Error updating cache: {error}")

    cache_update_event.set()
