import flet as ft
from .expansion_tiles_for_tab_menu import create_expansion_tile

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
            text='Orders',
            content=create_expansion_tile("Orders"),
            icon=ft.icons.BORDER_COLOR,
        ),
        ft.Tab(
            text='Enclosure',
            content=create_expansion_tile("Enclosure"),
            icon=ft.icons.ALL_INBOX,
        ),
        ft.Tab(
            text='TimeSheet',
            content=create_expansion_tile("TimeSheet"),
            icon=ft.icons.TABLE_ROWS_ROUNDED,
        ),
        ft.Tab(
            text='Companies',
            content=create_expansion_tile("Companies"),
            icon=ft.icons.HOME_WORK_SHARP,
        ),
        ft.Tab(
            text='Operators',
            content=create_expansion_tile("Operators"),
            icon=ft.icons.PEOPLE_SHARP,
        ),
        ft.Tab(
            text='Machines',
            content=create_expansion_tile("Machines"),
            icon=ft.icons.DRAW
        ),
    ]

    # If the user is 'admin' or 'superuser', add the "Users" and "ChangeLog" tabs
    if user_role in ['admin', 'super_user']:
        tabs.append(
            ft.Tab(
                text='Users',
                content=create_expansion_tile("Users"),
                icon=ft.icons.PERSON,
            )
        )
        tabs.append(
            ft.Tab(
                text='ChangeLog',
                content=create_expansion_tile("ChangeLog"),
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
