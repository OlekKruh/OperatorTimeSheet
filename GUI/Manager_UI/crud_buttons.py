import flet as ft
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from DataBase.crud import create_record
from DataBase.db_engine import get_session, get_engine
from GUI.Manager_UI.validate_prepare_forms import show_alert_dialog


def get_primary_key_column(model):
    """Возвращает имя столбца первичного ключа для модели."""
    for column in model.__table__.columns:
        if column.primary_key:
            return column.name


def record_exists(session: Session, model, **filters):
    """Проверяет, существует ли запись в базе данных с указанными фильтрами."""
    try:
        return session.query(model).filter_by(**filters).first() is not None
    except SQLAlchemyError as e:
        raise Exception(f"Error checking record existence: {e}")


def collect_form_data(fields_list):
    """Собирает значения полей формы, включая вложенные элементы, такие как Checkbox и Dropdown."""
    form_data = {}

    for field in fields_list:
        if hasattr(field, 'label') and isinstance(field, (ft.TextField, ft.Dropdown)):  # Для TextField и Dropdown
            form_data[field.label] = field.value
        elif isinstance(field, ft.Row):  # Для Row, которые содержат Checkboxes или другие элементы
            for control in field.controls:
                if isinstance(control, ft.Checkbox):
                    form_data[control.label] = control.value  # Сохранение значения чекбоксов
                elif isinstance(control, ft.Dropdown):
                    form_data[control.label] = control.value  # Сохранение значения выпадающих списков

    return form_data


def create_save_button(form_fields_list, validate_func, model):
    """Создаёт кнопку 'Save' и привязывает её к форме и валидации."""
    return ft.FilledButton(
        text='Save',
        on_click=lambda e: [
            e.page.update(),  # Обновляем страницу для получения актуальных значений
            handle_save(e, form_fields_list, validate_func, model)  # Обрабатываем сохранение
        ],
        style=ft.ButtonStyle(
            color=ft.colors.BLACK,
            bgcolor=ft.colors.WHITE,
        )
    )


def create_clear_button(fields_list):
    """Создаёт кнопку 'Clear', которая сбрасывает значения полей формы на значения по умолчанию."""
    return ft.FilledButton(
        text='Clear',
        on_click=lambda e: clear_form_fields(fields_list),
        style=ft.ButtonStyle(
            color=ft.colors.BLACK,
            bgcolor=ft.colors.WHITE,
        )
    )


def clear_form_fields(fields_list):
    # Проходим по каждому полю формы и очищаем его
    for field in fields_list:
        if isinstance(field, (ft.TextField, ft.Dropdown)):  # Для текстовых полей и выпадающих списков
            field.value = ""  # Очищаем значение
        elif isinstance(field, ft.Row):  # Для чекбоксов или других элементов в Row
            for control in field.controls:
                if isinstance(control, ft.Checkbox):
                    control.value = False  # Сбрасываем чекбоксы
                elif isinstance(control, ft.Dropdown):
                    control.value = ""  # Очищаем выпадающие списки
        field.update()  # Обновляем элемент интерфейса


def handle_save(e, form_fields_list, validate_func, model):
    # Сбор данных формы
    form_data = collect_form_data(form_fields_list)

    # Валидация данных
    validated_data = validate_func(e.page, form_data)

    # Если данные валидированы
    if validated_data:
        engine = get_engine()  # Создаём движок
        session = get_session(engine)  # Создаём сессию

        # Удаляем первичный ключ из данных перед проверкой на дубликаты
        primary_key_column = get_primary_key_column(model)
        if primary_key_column in validated_data:
            validated_data.pop(primary_key_column)

        # Проверка на существование записи с такими же полями
        if record_exists(session, model, **validated_data):
            show_alert_dialog(e.page, "Record with the same data already exists.")
            return

        # Если запись не существует, сохраняем её
        create_record(session, model, **validated_data)
        show_alert_dialog(e.page, "Record saved successfully")
