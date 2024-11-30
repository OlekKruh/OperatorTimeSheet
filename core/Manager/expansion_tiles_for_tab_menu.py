import flet as ft
from DataBase.models import model_mapping, get_pretty_name
from .crud_buttons import create_button
from .data_tables import create_data_table_automatically
from .form_fields import (
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
    "border_radius": 15,
}

# Универсальный словарь для валидации
VALIDATION_MAPPING = {
    'users': validate_user_form,
    'operator': validate_operator_form,
    'company': validate_company_form,
    'enclosure': validate_enclosure_form,
    'machine': validate_machine_form,
    'order': validate_order_form,
}

# Универсальный словарь для форм
FORM_FIELDS_MAPPING = {
    'users': user_form_fields_list,
    'operator': operator_form_fields_list,
    'company': company_form_fields_list,
    'enclosure': enclosure_form_fields_list,
    'machine': machine_form_fields_list,
    'order': order_form_fields_list,
}


def expansion_tiles(tab_title: str, mode: str = 'create'):
    """
    Создает универсальный ExpansionTile для работы с сущностью.
    Args:
        tab_title (str): Название вкладки.
        mode (str): Режим работы ('create' или 'delete_update').
    Returns:
        ft.ExpansionTile: Сконфигурированный компонент ExpansionTile.
    """
    model = model_mapping.get(tab_title)

    if not model:
        raise ValueError(f"Unsupported tab title: {tab_title}")

    if mode == 'create':
        return create_expansion_tile(tab_title)
    elif mode == 'delete_update':
        return delete_update_expansion_tile(tab_title)
    else:
        raise ValueError(f"Unsupported mode: {mode}")


def create_expansion_tile(tab_title: str):
    """
    Создает ExpansionTile для создания новой сущности.
    Args:
        tab_title (str): Название вкладки.
    Returns:
        ft.ExpansionTile: Сконфигурированный компонент ExpansionTile для создания.
    """

    pretty_title = get_pretty_name(tab_title)
    form_fields_list = FORM_FIELDS_MAPPING.get(tab_title, [])
    validate_func = VALIDATION_MAPPING.get(tab_title)

    if not validate_func:
        raise ValueError(f"Validation function not found for tab title: {tab_title}")

    save_button = create_button('save', form_fields_list,
                                validate_func, model_mapping[tab_title])
    clear_button = create_button('clear', form_fields_list)

    buttons_row = ft.Row(
        controls=[save_button, clear_button],
        alignment=ft.MainAxisAlignment.CENTER
    )

    return create_expansion_tile_base(
        title=f'Create New {pretty_title}',
        description=f'Fill out the form to create a new {pretty_title}. All fields must be completed.',
        content=ft.Container(
            ft.Column(
                controls=form_fields_list + [buttons_row],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=620,
            alignment=ft.alignment.center,
            **text_field_style
        )
    )


def delete_update_expansion_tile(tab_title: str):
    """
    Создает ExpansionTile для удаления или обновления сущности.
    Args:
        tab_title (str): Название вкладки.
    Returns:
        ft.ExpansionTile: Сконфигурированный компонент ExpansionTile для удаления/обновления.
    """

    pretty_title = get_pretty_name(tab_title)
    data_table = create_data_table_automatically(model_mapping[tab_title])

    return create_expansion_tile_base(
        title=f'Delete/Update {pretty_title}',
        description=f'Select a row to modify or delete {pretty_title}.',
        content=ft.Container(
            ft.Column(
                controls=[data_table],
            ),
            **text_field_style
        )
    )


def create_expansion_tile_base(title: str, description: str, content):
    """
    Базовая функция для создания компонента ExpansionTile.

    Args:
        title (str): Заголовок тайла.
        description (str): Описание тайла.
        content: Основной контент для тайла.

    Returns:
        ft.ExpansionTile: Базовый компонент ExpansionTile.
    """
    return ft.ExpansionTile(
        title=ft.Text(title, size=18, text_align=ft.TextAlign.CENTER),
        affinity=ft.TileAffinity.LEADING,
        collapsed_text_color=ft.colors.WHITE,
        text_color=ft.colors.WHITE,
        initially_expanded=True,
        controls=[
            ft.ListTile(
                title=ft.Text(description, text_align=ft.TextAlign.CENTER)
            ),
            content,
        ]
    )
