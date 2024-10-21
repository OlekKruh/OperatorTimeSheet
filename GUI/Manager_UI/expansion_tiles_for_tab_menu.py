import flet as ft
from DataBase.models import Order, Company, Operator, Machine, Enclosure, Users
from .crud_buttons import create_save_button, create_clear_button
from .forms import (
    order_form_fields_list,
    enclosure_form_fields_list,
    company_form_fields_list,
    operator_form_fields_list,
    machine_form_fields_list,
    user_form_fields_list,
)
from .validate_prepare_forms import (
    validate_order_form,
    validate_company_form,
    validate_operator_form,
    validate_machine_form,
    validate_enclosure_form,
    validate_user_form
)

# Common style settings for text fields and container alignment.
text_field_style = {
    "padding": ft.Padding(left=10, right=10, top=10, bottom=10),
    "bgcolor": ft.colors.LIGHT_BLUE_700,
    "alignment": ft.alignment.center_left
}


def create_new_expansion_tile(tab_title: str, validate_form):
    """
    Creates an expansion tile for creating a new entity.

    Args:
        tab_title (str): The title of the tab to be displayed, e.g., "Orders", "Companies", etc.
        validate_form:

    Returns:
        ft.ExpansionTile: ExpansionTile for creating a new entity.

    """

    # Словари для сопоставления заголовков вкладок с моделями и функциями валидации
    model_mapping = {
        'Orders': Order,
        'Companies': Company,
        'Operators': Operator,
        'Machines': Machine,
        'Enclosure': Enclosure,
        'Users': Users,
        # Добавь другие модели по мере необходимости
    }

    validation_mapping = {
        'Orders': validate_order_form,
        'Companies': validate_company_form,
        'Operators': validate_operator_form,
        'Machines': validate_machine_form,
        'Enclosure': validate_enclosure_form,
        'Users': validate_user_form,
        # Добавь другие функции валидации по мере необходимости
    }

    # Получаем соответствующую модель и функцию валидации по заголовку вкладки
    model = model_mapping.get(tab_title)
    validate_func = validation_mapping.get(tab_title)

    if not model or not validate_func:
        raise ValueError(f"Unsupported tab title: {tab_title}")

    # Получаем список полей формы
    form_fields_list = form_selection(tab_title)

    # Создаём кнопку Save, передаём список полей для валидации
    save_button = create_save_button(form_fields_list, validate_func, model)
    clear_button = create_clear_button(form_fields_list)

    # Создаём контейнер с кнопками в ряд
    buttons_row = ft.Row(
        controls=[save_button, clear_button],
        alignment=ft.MainAxisAlignment.START
    )

    # Возвращаем универсальный тайл с формой и кнопкой Save
    return ft.ExpansionTile(
        title=ft.Text(f'Create New {tab_title}', size=18),
        affinity=ft.TileAffinity.LEADING,
        collapsed_text_color=ft.colors.WHITE,
        text_color=ft.colors.WHITE,
        initially_expanded=True,
        controls=[
            ft.ListTile(
                title=ft.Text(f'Fill out the form to create a new {tab_title}.\nAll fields must be completed.')),
            ft.Container(ft.Column(controls=form_fields_list + [buttons_row]), **text_field_style)
        ]
    )


def delete_update_expansion_tile(tab_title: str):
    """
    Creates an expansion tile for deleting or updating an entity.

    Args:
        tab_title (str): The title of the tab to be displayed, e.g., "Orders", "Companies", etc.

    Returns:
        ft.ExpansionTile: ExpansionTile for deleting or updating an entity.
    """
    return ft.ExpansionTile(
        title=ft.Text(f'Delete/Update {tab_title}', size=18),
        affinity=ft.TileAffinity.LEADING,
        collapsed_text_color=ft.colors.WHITE,
        text_color=ft.colors.WHITE,
        controls=[
            ft.ListTile(title=ft.Text(f'Select a row to modify or delete {tab_title}.')),
            ft.ListTile(title=ft.Text("IN PROGRESS"))  # Здесь нужно заменить на актуальный функционал
        ]
    )


def form_selection(tab_title: str):
    """
    Returns a list of form fields based on the tab title.

    Args:
        tab_title (str): The title of the tab (e.g., 'Orders', 'Companies', etc.).

    Returns:
        list: A list containing the corresponding form fields.
    """
    match tab_title:
        case 'Orders':
            return order_form_fields_list  # Возвращаем список полей
        case 'Enclosure':
            return enclosure_form_fields_list  # Возвращаем список полей
        case 'Companies':
            return company_form_fields_list  # Возвращаем список полей
        case 'Operators':
            return operator_form_fields_list  # Возвращаем список полей
        case 'Machines':
            return machine_form_fields_list  # Возвращаем список полей
        case 'Users':
            return user_form_fields_list  # Возвращаем список полей
        case 'TimeSheet':
            return []  # Пустой список для временных данных
        case 'ChangeLog':
            return []  # Пустой список для временных данных
        case _:
            return []
