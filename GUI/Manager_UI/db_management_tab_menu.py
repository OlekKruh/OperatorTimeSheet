import flet as ft
from .expansion_tiles_for_tab_menu import create_new_expansion_tile, delete_update_expansion_tile
from .validate_prepare_forms import (
    validate_user_form,
    validate_order_form,
    validate_enclosure_form,
    validate_company_form,
    validate_operator_form,
    validate_machine_form
)

name = 'DB manager'


def db_management_tab_menu(user_role: str):
    """
    Creates the DB Manager tab menu. Tabs “Users” and “ChangeLog”
    are visible only for users with roles 'admin' or 'superuser'.

     Args:
        user_role: The role of the logged-in user ('admin', 'superuser', 'manager', 'operator').
    """

    # Create a list of tabs that are always visible
    tabs = [
        ft.Tab(
            text='TimeSheet',
            content=ft.ListTile(
                    title=ft.Text("TimeSheet viewing is currently under development")
                ),
            icon=ft.icons.TABLE_ROWS_ROUNDED,
        ),
        ft.Tab(
            text='Orders',
            content=ft.Column(
                controls=[
                    create_new_expansion_tile("Orders", validate_order_form),
                    delete_update_expansion_tile("Orders")
                ],
                scroll=ft.ScrollMode.ALWAYS
            ),
            icon=ft.icons.BORDER_COLOR,
        ),
        ft.Tab(
            text='Enclosure',
            content=ft.Column(
                controls=[
                    create_new_expansion_tile("Enclosure", validate_enclosure_form),
                    delete_update_expansion_tile("Enclosure")
                ],
                scroll=ft.ScrollMode.ALWAYS
            ),
            icon=ft.icons.ALL_INBOX,
        ),
        ft.Tab(
            text='Companies',
            content=ft.Column(
                controls=[
                    create_new_expansion_tile("Companies", validate_company_form),
                    delete_update_expansion_tile("Companies")
                ],
                scroll=ft.ScrollMode.ALWAYS
            ),
            icon=ft.icons.HOME_WORK_SHARP,
        ),
        ft.Tab(
            text='Operators',
            content=ft.Column(
                controls=[
                    create_new_expansion_tile("Operators", validate_operator_form),
                    delete_update_expansion_tile("Operators")
                ],
                scroll=ft.ScrollMode.ALWAYS
            ),
            icon=ft.icons.PEOPLE_SHARP,
        ),
        ft.Tab(
            text='Machines',
            content=ft.Column(
                controls=[
                    create_new_expansion_tile("Machines", validate_machine_form),
                    delete_update_expansion_tile("Machines")
                ],
                scroll=ft.ScrollMode.ALWAYS
            ),
            icon=ft.icons.DRAW
        ),
    ]

    # If the user is 'admin' or 'superuser', add the "Users" and "ChangeLog" tabs
    if user_role in ['admin', 'super_user']:
        tabs.append(
            ft.Tab(
                text='Users',
                content=ft.Column(
                    controls=[
                        create_new_expansion_tile("Users", validate_user_form),
                        delete_update_expansion_tile("Users")
                    ],
                    scroll=ft.ScrollMode.ALWAYS
                ),
                icon=ft.icons.PERSON,
            )
        )
        tabs.append(
            ft.Tab(
                text='ChangeLog',
                content=ft.ListTile(
                    title=ft.Text("ChangeLog viewing is currently under development")
                ),
                icon=ft.icons.HISTORY,
            )
        )

    # Return the Tabs component with the appropriate tabs
    return ft.Tabs(
        selected_index=0,
        animation_duration=400,
        tabs=tabs,
        expand=True,
        indicator_color=ft.colors.GREEN_ACCENT_400,
        divider_color=ft.colors.WHITE,
        label_color=ft.colors.GREEN_ACCENT_400,
    )
