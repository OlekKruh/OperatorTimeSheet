import asyncio
import datetime
from .models import model_mapping
from .db_engine import get_db_session
from DataBase.models import ChangeLog


def cache_manager():
    _cache_data = {}

    def initialize_cache():
        """Инициализирует кеш данными из базы данных при запуске."""
        with get_db_session() as session:
            for tab_name, model in model_mapping.items():
                _cache_data[tab_name] = session.query(model).all()  # Сохраняем объекты SQLAlchemy
        print(f"Cache initialized:, {_cache_data}\n")

    def get_cache(tab_name):
        """Возвращает данные кеша для указанной таблицы."""
        data = _cache_data.get(tab_name, [])
        print(f"Data retrieved from cache for '{tab_name}': {data}")  # Выводим данные для отладки
        return data

    def add_to_cache(tab_name, record):
        """Добавляет новую запись или список записей в кеш. Инициализирует кеш для таблицы, если его нет."""
        if tab_name not in _cache_data:
            _cache_data[tab_name] = []  # Инициализируем пустой список, если отсутствует
        _cache_data[tab_name].append(record)
        print(f"Initialized cache for table '{tab_name}'")

    def update_cache(tab_name, record_id, updated_record):
        """Обновляет существующую запись в кэше."""
        for idx, record in enumerate(_cache_data.get(tab_name, [])):
            if getattr(record, 'id', None) == record_id:  # Проверяем по ID записи
                _cache_data[tab_name][idx] = updated_record
                print(f"Updated record in cache for '{tab_name}': {updated_record}")
                return
        print(f"Record with ID {record_id} not found in cache for '{tab_name}'.")

    def delete_from_cache(tab_name, record_id):
        """Удаляет запись из кэша по ID."""
        _cache_data[tab_name] = [record for record in _cache_data.get(tab_name, []) if
                                 getattr(record, 'id', None) != record_id]
        print(f"Deleted record with ID {record_id} from cache for '{tab_name}'.")

    return initialize_cache, get_cache, add_to_cache, update_cache, delete_from_cache


initialize_cache, get_cache, add_to_cache, update_cache, delete_from_cache = cache_manager()


async def poll_change_log():
    """Асинхронно опрашивает таблицу ChangeLog каждые 60 секунд и обновляет кэш."""
    last_check_time = datetime.datetime.now(datetime.UTC)  # Инициализация времени последней проверки
    while True:
        await asyncio.sleep(60)
        with get_db_session() as session:
            last_check_time = check_and_update_cache(session, last_check_time)


def check_and_update_cache(session, last_check_time):
    """Проверяет таблицу ChangeLog и обновляет кэш на основе найденных изменений."""
    # Запрашиваем изменения, произошедшие с момента последней проверки
    changes = session.query(ChangeLog).filter(ChangeLog.changed_at > last_check_time).all()
    last_check_time = datetime.datetime.now(datetime.UTC)

    for change in changes:
        original_tab_name = change.table_name  # Таблица, в которой произошло изменение
        model = model_mapping.get(original_tab_name)  # Получаем модель для таблицы

        if not model:
            print(f"Warning: Model for table '{original_tab_name}' not found in model_mapping.")
            continue

        operation = change.operation_type
        record_id = change.record_id

        # Выполнение операции в зависимости от типа
        match operation:
            case 'INSERT':
                new_data = session.query(model).get(record_id)
                if new_data:
                    add_to_cache(original_tab_name, new_data)  # Добавление в кэш
            case 'UPDATE':
                updated_data = session.query(model).get(record_id)
                if updated_data:
                    update_cache(original_tab_name, record_id, updated_data)  # Обновление в кэше
            case 'DELETE':
                delete_from_cache(original_tab_name, record_id)  # Удаление из кэша

        print(f"Cache updated for '{original_tab_name}': {get_cache(original_tab_name)}")

    return last_check_time
