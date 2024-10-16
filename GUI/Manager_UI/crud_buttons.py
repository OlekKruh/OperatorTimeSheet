import flet as ft


def collect_form_data(fields_list):
    """Собирает значения полей из списка в словарь."""
    return {field.label: field.value for field in fields_list if hasattr(field, 'label')}


def create_save_button(form_fields_list, validate_func):
    """Создаёт кнопку 'Save' и привязывает её к форме."""
    return ft.FilledButton(
        text='Save',
        on_click=lambda e: [
            e.page.update(),  # Обновляем страницу для получения актуальных значений
            validate_func(e.page, collect_form_data(form_fields_list))  # Передаём объект страницы и данные формы
        ],
        style=ft.ButtonStyle(
            color=ft.colors.BLACK,
            bgcolor=ft.colors.WHITE,
        )
    )


