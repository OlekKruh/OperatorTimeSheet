import flet as ft
from .forms_create_modify import user_form, company_form, enclosure_form, machine_form, order_form, operator_form


def create_expansion_tile(tab_title: str):
    return ft.Column(
        controls=[
            ft.ExpansionTile(
                title=ft.Text(f'Create New {tab_title}', size=18),
                affinity=ft.TileAffinity.LEADING,
                collapsed_text_color=ft.colors.WHITE,
                text_color=ft.colors.WHITE,
                controls=[
                    ft.ListTile(title=ft.Text(f'Fill out the form to create a new {tab_title}.')),
                    form_selection(tab_title)
                ]
            ),
            ft.ExpansionTile(
                title=ft.Text(f'Delete/Update {tab_title}', size=18),
                affinity=ft.TileAffinity.LEADING,
                collapsed_text_color=ft.colors.WHITE,
                text_color=ft.colors.WHITE,
                controls=[
                    ft.ListTile(title=ft.Text(f'Select a row to modify or delete {tab_title}.')),
                    ft.ListTile(title=ft.Text("IN PROGRESS"))  # заменить на функционал,
                ]
            ),
        ]
    )


text_field_style = {
    "padding": ft.Padding(left=10, right=10, top=10, bottom=10),
    "bgcolor": ft.colors.LIGHT_BLUE_700,
}


def form_selection(tab_title: str):
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

