import json
from datetime import datetime

import flet as ft
from sqlalchemy.orm import Session

# Карты сопоставления для заголовков столбцов
USER_FIELD_TITLE_MAPPING = {
    'user_id': "User ID",
    'access_login': "Access\nLogin",
    'hash_pass': "Password\nHash",
    'is_superuser': "Superuser"
}

OPERATOR_FIELD_TITLE_MAPPING = {
    'operator_id': "Operator\nID",
    'operator_name': "Name",
    'skill': "Skill\nLevel"
}

COMPANY_FIELD_TITLE_MAPPING = {
    'company_id': "Company\nID",
    'sap_id': "SAP\nID",
    'company_title': "Company\nTitle",
    'company_country': "Company\nCountry",
    'company_shipping_address': "Shipping\nAddress",
    'company_phone': "Contact\nPhone",
    'company_email': "Email"
}

ENCLOSURE_FIELD_TITLE_MAPPING = {
    'enclosure_id': "Enclosure\nID",
    'sap_id': "SAP\nID",
    'enclosure_title': "Enclosure\nTitle",
    'base': "Base",
    'cover': "Cover",
    'panel': "Panel",
    'filter': "Filter",
    'slot_mask': "Slot\nMask",
    'pcb': "PCB Mount\nPlate"
}

MACHINE_FIELD_TITLE_MAPPING = {
    'machine_id': "Machine\nID",
    'sap_id': "SAP\nID",
    'machine_title': "Title",
    'machine_serial_number': "Serial\nNumber",
    'machine_manufacturer': "Manufacturer",
    'machine_year_production': "Production\nYear"
}

ORDER_FIELD_TITLE_MAPPING = {
    'order_id': "Order\nID",
    'company_id': "Company\nID",
    'enclosure_id': "Enclosure\nID",
    'variant': "Variant",
    'order_quantity': "Order\nQuantity",
    'operation_quantity': "Operations\nQuantity",
    'operation_description': "Operation\nDescription",
    'order_cost': "Order\nCost",
    'order_received_date': "Received\nDate"
}

TIMESHEET_FIELD_TITLE_MAPPING = {
    'row_id': "Row\nID",
    'user_id': "User\nID",
    'operator_id': "Operator\nID",
    'start_time': "Start\nTime",
    'stop_time': "Stop\nTime",
    'order_id': "Order\nID",
    'operation': "Operation",
    'quantity_done': "Quantity\nDone",
    'damaged_enclosures': "Damaged\nEnclosures",
    'cause_of_damage': "Cause of\nDamage",
    'note_description': "Note",
    'machine_id': "Machine ID"
}

CHANGELOG_FIELD_TITLE_MAPPING = {
    'log_id': "Log\nID",
    'table_name': "Table\nName",
    'record_id': "Record\nID",
    'operation_type': "Operation\nType",
    'changed_at': "Changed\nAt",
    'user_id': "User\nID",
    'old_values': "Old\nValues",
    'new_values': "New\nValues"
}


def format_datetime(value):
    """
    Форматирует дату и время, убирая миллисекунды.
    """
    if isinstance(value, datetime):
        return value.strftime("%d-%m-%Y %H:%M:%S")  # Формат без миллисекунд
    return str(value)  # Возвращаем значение как есть, если это не datetime


def format_dict(value):
    """
    Форматирует словарь в читаемый формат JSON.
    """
    if isinstance(value, dict):
        return json.dumps(value, indent=4, ensure_ascii=False)  # Читаемый JSON с отступами
    return str(value)


def load_data_from_db(model, session: Session):
    """
    Загружает данные из базы данных для заданной модели.

    Args:
        model: Модель SQLAlchemy, на основе которой строится таблица.
        session: Сессия SQLAlchemy для выполнения запросов.

    Returns:
        list: Список записей модели.
    """
    try:
        # Загружаем все записи модели
        records = session.query(model).all()
        return records
    except Exception as e:
        print(f"Error loading data: {e}")
        return []


# Функция для автоматического создания DataTable на основе модели SQLAlchemy
def create_data_table_automatically(model, session: Session):
    """
    Автоматически создает DataTable на основе модели SQLAlchemy с настройками текста.
    """
    # Загружаем все записи из таблицы модели
    records = load_data_from_db(model, session)

    # Определение соответствующей карты заголовков
    field_title_mapping = get_field_title_mapping_for_model(model)

    # Извлекаем имена колонок из модели и преобразуем их в удобные названия
    columns = [
        ft.DataColumn(
            label=ft.Container(
                content=ft.Text(
                    field_title_mapping.get(column.name, column.name).strip(),
                    size=14,
                    color="black",
                    text_align=ft.TextAlign.CENTER,
                ),
                alignment=ft.alignment.center,  # Центрируем заголовки колонок
                width=90  # Задаем фиксированную ширину (можете подкорректировать под нужный размер)
            ),
            tooltip=field_title_mapping.get(column.name, column.name),
        )
        for column in model.__table__.columns
    ]

    # Создаем строки данных, извлекая значения атрибутов из каждой записи
    pading_n = 2
    rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Container(
                        content=ft.Text(
                            value=format_dict(getattr(record, column.name))
                            if column.name in ["old_values", "new_values"] else
                            format_datetime(getattr(record, column.name)),
                            size=12,
                            color="black",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.alignment.center,  # Центрируем текст в ячейках
                        padding=ft.Padding(pading_n, pading_n, pading_n, pading_n),
                    )
                )
                for column in model.__table__.columns
            ]
        )
        for record in records
    ]

    # Возвращаем готовую таблицу
    return ft.DataTable(
        columns=columns,
        rows=rows,
        bgcolor='white',
        border=ft.border.all(2, "black"),
        vertical_lines=ft.BorderSide(1, "black"),
        horizontal_lines=ft.BorderSide(1, "black"),
        border_radius=10,

    )


def get_field_title_mapping_for_model(model):
    """
    Возвращает карту заголовков для заданной модели.

    Args:
        model: Модель SQLAlchemy.

    Returns:
        dict: Словарь сопоставления заголовков полей.
    """
    # Соответствие моделей их картам полей
    if model.__name__ == 'Users':
        return USER_FIELD_TITLE_MAPPING
    elif model.__name__ == 'Operator':
        return OPERATOR_FIELD_TITLE_MAPPING
    elif model.__name__ == 'Company':
        return COMPANY_FIELD_TITLE_MAPPING
    elif model.__name__ == 'Enclosure':
        return ENCLOSURE_FIELD_TITLE_MAPPING
    elif model.__name__ == 'Machine':
        return MACHINE_FIELD_TITLE_MAPPING
    elif model.__name__ == 'Order':
        return ORDER_FIELD_TITLE_MAPPING
    elif model.__name__ == 'TimeSheet':
        return TIMESHEET_FIELD_TITLE_MAPPING
    elif model.__name__ == 'ChangeLog':
        return CHANGELOG_FIELD_TITLE_MAPPING
    else:
        return {}
