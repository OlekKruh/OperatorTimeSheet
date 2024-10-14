import flet as ft
from .forms_create_modify import user_form, company_form, enclosure_form, machine_form, order_form, operator_form


def create_new_expansion_tile(tab_title: str):
    """
    Creates an expansion tile for creating a new entity.

    Args:
        tab_title (str): The title of the tab to be displayed, e.g., "Orders", "Companies", etc.

    Returns:
        ft.ExpansionTile: ExpansionTile for creating a new entity.
    """
    return ft.ExpansionTile(
        title=ft.Text(f'Create New {tab_title}', size=18),
        affinity=ft.TileAffinity.LEADING,
        collapsed_text_color=ft.colors.WHITE,
        text_color=ft.colors.WHITE,
        controls=[
            ft.ListTile(
                title=ft.Text(f'Fill out the form to create a new {tab_title}.\nAll fields must be completed.')),
            form_selection(tab_title)  # Предполагается, что эта функция уже существует и возвращает форму
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


# Common style settings for text fields and container alignment.
text_field_style = {
    "padding": ft.Padding(left=10, right=10, top=10, bottom=10),
    "bgcolor": ft.colors.LIGHT_BLUE_700,
    "alignment": ft.alignment.center_left
}


def form_selection(tab_title: str):
    """
    Returns a container with the appropriate form based on the tab title.

    Args:
        tab_title (str): The title of the tab (e.g., 'Orders', 'Companies', etc.).

    Returns:
        ft.Container: A container containing the corresponding form or a message if the form is not available.
    """
    match tab_title:
        case 'Orders':
            return ft.Container(
                content=ft.Column(order_form()),
                **text_field_style
            )
        case 'Enclosure':
            return ft.Container(
                content=ft.Column(enclosure_form()),
                **text_field_style
            )
        case 'Companies':
            return ft.Container(
                content=ft.Column(company_form()),
                **text_field_style
            )
        case 'Operators':
            return ft.Container(
                content=ft.Column(operator_form()),
                **text_field_style
            )
        case 'Machines':
            return ft.Container(
                content=ft.Column(machine_form()),
                **text_field_style
            )
        case 'Users':
            return ft.Container(
                content=ft.Column(user_form()),
                **text_field_style
            )
        case 'TimeSheet':
            return ft.Container(
                content=ft.Text("Form in progress"),
                **text_field_style
            )
        case 'ChangeLog':
            return ft.Container(
                content=ft.Text("Form in progress"),
                **text_field_style
            )
        case _:
            return ft.Container(
                content=ft.Text("Error"),
                **text_field_style
            )
