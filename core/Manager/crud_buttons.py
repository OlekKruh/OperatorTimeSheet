import flet as ft
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataBase.crud import create_record
from DataBase.db_engine import get_db_session
from .validate_prepare_forms import show_alert_dialog
from DataBase.cache_manager import crud_update_cache


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


def create_button(button_type: str, form_fields_list=None, validate_func=None, model=None) -> ft.FilledButton:
    """Создаёт универсальную кнопку в зависимости от типа."""

    def handle_action(e):
        form_data = collect_form_data(form_fields_list)
        validated_data = validate_func(e.page, form_data) if validate_func else form_data

        match button_type:
            case 'save':
                if validated_data:
                    save_data_to_database(e, model, validated_data)
            case 'update':
                if validated_data:
                    update_data_in_database(e, model, validated_data)
                pass
            case 'delete':
                delete_data_from_database(e, model, form_data)
                pass
            case 'clear':
                clear_form_fields(form_fields_list)
            case _:
                show_alert_dialog(e.page, f'Unknown button type: {button_type}')

    button_text = button_type.capitalize()
    return ft.FilledButton(
        text=button_text,
        on_click=handle_action,
        style=ft.ButtonStyle(
            color=ft.colors.BLACK,
            bgcolor=ft.colors.WHITE,
        )
    )


def save_data_to_database(e, model, validated_data):
    """Сохраняет запись в базе данных, если её нет."""
    with get_db_session() as session:
        try:
            primary_key_column = get_primary_key_column(model)
            if primary_key_column and primary_key_column in validated_data:
                validated_data.pop(primary_key_column)
                if record_exists(session, model, **validated_data):
                    show_alert_dialog(e.page, "Record with the same data already exists.")
                else:
                    create_record(session, model, **validated_data)
                    show_alert_dialog(e.page, "Record saved successfully")
                    crud_update_cache()
        except SQLAlchemyError as error:
            show_alert_dialog(e.page, f"Error saving record: {error}")


def update_data_in_database(e, model, validated_data):
    """Обновляет данные в базе данных с использованием сессии."""
    with get_db_session() as session:
        try:
            primary_key_column = get_primary_key_column(model)
            if primary_key_column and primary_key_column in validated_data:
                record = session.query(model).get(validated_data[primary_key_column])
                if record:
                    for key, value in validated_data.items():
                        setattr(record, key, value)
                    session.commit()
                    show_alert_dialog(e.page, "Record updated successfully")
                    crud_update_cache()
                else:
                    show_alert_dialog(e.page, "Record not found for update.")
        except SQLAlchemyError as error:
            show_alert_dialog(e.page, f"Error updating record: {error}")


def delete_data_from_database(e, model, form_data):
    """Удаляет запись из базы данных с использованием сессии."""
    with get_db_session() as session:
        try:
            primary_key_column = get_primary_key_column(model)
            if primary_key_column and primary_key_column in form_data:
                record = session.query(model).get(form_data[primary_key_column])
                if record:
                    session.delete(record)
                    session.commit()
                    show_alert_dialog(e.page, "Record deleted successfully")
                    crud_update_cache()
                else:
                    show_alert_dialog(e.page, "Record not found for deletion.")
        except SQLAlchemyError as error:
            show_alert_dialog(e.page, f"Error deleting record: {error}")


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
