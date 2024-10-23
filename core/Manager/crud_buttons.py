import flet as ft
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataBase.crud import create_record
from DataBase.db_engine import get_db_session
from .validate_prepare_forms import show_alert_dialog


def get_primary_key_column(model) -> str:
    """Возвращает имя столбца первичного ключа для модели."""
    return next((column.name for column in model.__table__.columns if column.primary_key), None)


def record_exists(session: Session, model, **filters) -> bool:
    """Проверяет, существует ли запись в базе данных с указанными фильтрами."""
    try:
        return session.query(model).filter_by(**filters).first() is not None
    except SQLAlchemyError as e:
        raise Exception(f"Error checking record existence: {e}")


def collect_form_data(fields_list) -> dict:
    """Собирает значения полей формы, включая вложенные элементы, такие как Checkbox и Dropdown."""
    form_data = {}

    for field in fields_list:
        if isinstance(field, (ft.TextField, ft.Dropdown)) and hasattr(field, 'label'):
            form_data[field.label] = field.value
        elif isinstance(field, ft.Row):
            for control in field.controls:
                if isinstance(control, (ft.Checkbox, ft.Dropdown)):
                    form_data[control.label] = control.value

    return form_data


def create_button(text: str, on_click, color=ft.colors.BLACK, bgcolor=ft.colors.WHITE) -> ft.FilledButton:
    """Создаёт универсальную кнопку."""
    return ft.FilledButton(
        text=text,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=color,
            bgcolor=bgcolor,
        )
    )


def create_save_button(form_fields_list, validate_func, model) -> ft.FilledButton:
    """Создаёт кнопку 'Save' и привязывает её к форме и валидации."""
    return create_button(
        text='Save',
        on_click=lambda e: handle_save(e, form_fields_list, validate_func, model)
    )


def create_clear_button(form_fields_list) -> ft.FilledButton:
    """Создаёт кнопку 'Clear', которая сбрасывает значения полей формы на значения по умолчанию."""
    return create_button(
        text='Clear',
        on_click=lambda e: clear_form_fields(form_fields_list)
    )


def clear_form_fields(fields_list):
    """Очищает все поля формы, устанавливая значения по умолчанию."""
    for field in fields_list:
        if isinstance(field, (ft.TextField, ft.Dropdown)):
            field.value = ""  # Очищаем значение
        elif isinstance(field, ft.Row):
            for control in field.controls:
                if isinstance(control, ft.Checkbox):
                    control.value = False
                elif isinstance(control, ft.Dropdown):
                    control.value = ""
        field.update()


def handle_save(e, form_fields_list, validate_func, model):
    """Обрабатывает событие сохранения данных формы."""
    form_data = collect_form_data(form_fields_list)

    # Валидация данных
    validated_data = validate_func(e.page, form_data)

    if validated_data:
        save_data_to_database(e, model, validated_data)


def save_data_to_database(e, model, validated_data):
    """Сохраняет данные в базу данных с использованием сессии."""
    with get_db_session() as session:
        save_record(e, session, model, validated_data)


def save_record(e, session, model, validated_data):
    """Сохраняет запись в базе данных, если её нет."""
    primary_key_column = get_primary_key_column(model)
    if primary_key_column and primary_key_column in validated_data:
        validated_data.pop(primary_key_column)

    if record_exists(session, model, **validated_data):
        show_alert_dialog(e.page, "Record with the same data already exists.")
    else:
        try:
            create_record(session, model, **validated_data)
            show_alert_dialog(e.page, "Record saved successfully")
        except SQLAlchemyError as error:
            show_alert_dialog(e.page, f"Error saving record: {error}")


