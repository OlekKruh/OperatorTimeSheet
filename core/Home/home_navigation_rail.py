import flet as ft
import asyncio
from core.constants import *
from DataBase.session_manager import clear_user_session
from core.History.history_container import history_elements
from core.Settings.settings_container import settings_elements
from core.Manager.db_management_tab_menu import db_management_tab_menu


def home_elements(page: ft.Page, user_role: str):
    """
    Sets up the main Home Screen of the application with a persistent
    Navigation Rail, and a default display of history elements based on user roles.

    Args:
        page (ft.Page): The Flet page object that will display the home screen.
        user_role (str): Role of the logged-in user ('admin', 'manager', 'operator').
    """
    # Clean the page before adding new elements
    page.clean()

    # Create a column to display the content based on the selected tab
    content_column = ft.Column(
        controls=[],
        alignment=ft.MainAxisAlignment.START,
    )

    # Define the NavigationRail with its destinations
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        group_alignment=0,
        min_width=50,
        bgcolor=ROJAL_MARIN,
        indicator_color=ft.colors.WHITE,
        destinations=[
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.HISTORY),
                selected_icon_content=ft.Icon(ft.icons.HISTORY, color=ROJAL_MARIN),
                label_content=ft.Text("History")
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.TABLE_ROWS_ROUNDED),
                selected_icon_content=ft.Icon(ft.icons.TABLE_ROWS_ROUNDED, color=ROJAL_MARIN),
                label_content=ft.Text("Timesheet")
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.INSERT_CHART),
                selected_icon_content=ft.Icon(ft.icons.INSERT_CHART, color=ROJAL_MARIN),
                label_content=ft.Text("Statistics")
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.MENU_BOOK),
                selected_icon_content=ft.Icon(ft.icons.MENU_BOOK, color=ROJAL_MARIN),
                label_content=ft.Text("DB\nManager", text_align=ft.TextAlign.CENTER)
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.SEARCH),
                selected_icon_content=ft.Icon(ft.icons.SEARCH, color=ROJAL_MARIN),
                label_content=ft.Text("Search")
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.SETTINGS),
                selected_icon_content=ft.Icon(ft.icons.SETTINGS, color=ROJAL_MARIN),
                label_content=ft.Text("Settings")
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.LOGOUT, color=ft.colors.RED),
                selected_icon_content=ft.Icon(ft.icons.LOGOUT, color=ft.colors.RED),
                label_content=ft.Text("Exit")
            ),
        ],
        on_change=lambda e: asyncio.run(on_rail_change(e, content_column, page, user_role, rail)),
    )

    # Add the Navigation Rail and content column to the page layout
    page.add(
        ft.Row(
            [
                ft.Container(
                    content=rail,
                    margin=0.5,
                    padding=0.5,
                    alignment=ft.alignment.center_left,
                    bgcolor=ROJAL_MARIN,
                    width=80,
                    border_radius=10
                ),
                ft.Container(
                    content=content_column,
                    margin=0.5,
                    padding=0.5,
                    alignment=ft.alignment.top_left,
                    expand=True,
                    bgcolor=ROJAL_MARIN,
                    border_radius=10
                )
            ],
            expand=True
        )
    )

    # Display history elements by default
    history_elements(content_column)

    # Update the page to reflect the new layout
    page.update()


async def on_rail_change(e, content_column, page, user_role: str, rail: ft.NavigationRail):
    """
    Handles the logic for updating the content area when a new tab is selected
    in the NavigationRail, while respecting user role permissions.

    Args:
        e: Event object containing the selected tab index.
        content_column: The column to display the selected tab's content.
        page: The Flet page object to allow window control actions like closing.
        user_role: Role of the logged-in user ('admin', 'superuser', 'manager', 'operator').
        rail: The NavigationRail component for controlling navigation.
    """
    selected_index = e.control.selected_index

    # Clear the current content
    content_column.controls.clear()

    # Add a loading indicator centered in the container
    loading_indicator = ft.ProgressRing()
    content_column.controls.append(
        ft.Container(
            content=loading_indicator,
            alignment=ft.alignment.center,  # Центрируем колесо загрузки
            expand=True
        )
    )
    content_column.update()

    # Create a reusable Access Denied dialog
    def show_access_denied_dialog(message):
        content_column.controls.clear()
        content_column.controls.append(ft.Text(message, size=20, color=ft.colors.RED))
        content_column.update()

    # Load content based on selected tab index and user role permissions
    match selected_index:
        case 0:
            # History tab
            content_column.controls.clear()
            history_elements(content_column)
        case 1:
            # Timesheet tab
            content_column.controls.clear()
            content_column.controls.append(ft.Text("Timesheet Content", size=20))
        case 2:
            # Statistics tab
            content_column.controls.clear()
            content_column.controls.append(ft.Text("Statistics Content", size=20))
        case 3:
            # DB Manager tab (only available to 'admin' and 'manager')
            if user_role == 'operator':
                show_access_denied_dialog("Access Denied: You do not have access to DB Manager")
            else:
                content_column.controls.clear()
                db_manager_tabs = db_management_tab_menu(user_role)
                content_column.controls.append(db_manager_tabs)
        case 4:
            # Search tab
            content_column.controls.clear()
            content_column.controls.append(ft.Text("Search Content", size=20))
        case 5:
            # Settings tab (only available to 'admin' or 'super_user')
            if user_role not in ['admin', 'super_user']:
                show_access_denied_dialog("Access Denied: You do not have access to Settings")
            else:
                content_column.controls.clear()
                settings_elements(content_column, page)
        case 6:
            # Exit the application
            clear_user_session()
            page.window_close()

    # Если контент пуст, показать заглушку
    if not content_column.controls:
        content_column.controls.append(ft.Text("No content available", size=20, color=ft.colors.GREY))

    # Обновление содержимого
    content_column.update()
    page.update()
