import flet as ft
from GUI.constants import *
from GUI.History_UI.history_container import history_elements
from GUI.Settings_UI.settings_container import settings_elements
from GUI.Manager_UI.db_management_tab_menu import db_management_tab_menu


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
    content_column = ft.Column()

    # Define the NavigationRail with its destinations
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        group_alignment=0,
        min_width=50,
        bgcolor=ROJAL_MARIN,
        indicator_color=WIGHT,
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
                icon_content=ft.Icon(ft.icons.LOGOUT, color=RED),
                selected_icon_content=ft.Icon(ft.icons.LOGOUT, color=RED),
                label_content=ft.Text("Exit")
            ),
        ],
        on_change=lambda e: on_rail_change(e, content_column, page, user_role, rail),
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


def on_rail_change(e, content_column, page, user_role: str, rail: ft.NavigationRail):
    """
    Handles the logic for updating the content area when a new tab is selected
    in the NavigationRail, while respecting user role permissions.

    Args:
        e: Event object containing the selected tab index.
        content_column: The column to display the selected tab's content.
        page: The Flet page object to allow window control actions like closing.
        user_role: Role of the logged-in user ('admin', 'manager', 'operator').
        rail: The NavigationRail component for controlling navigation.
    """
    selected_index = e.control.selected_index

    # Clear the current content
    content_column.controls.clear()

    # Create a reusable Access Denied dialog
    def show_access_denied_dialog(message):
        dialog = ft.AlertDialog(
            title=ft.Text("Access Denied"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda _: close_dialog(dialog))],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Function to close the dialog and revert to the first tab (index 0)
    def close_dialog(dialog):
        dialog.open = False
        page.update()
        rail.selected_index = 0
        rail.update()

    # Switch based on the selected index and check user role permissions
    match selected_index:
        case 0:
            # History tab
            history_elements(content_column)
        case 1:
            # Input tab
            content_column.controls.append(ft.Text("Timesheet"))
        case 2:
            # Statistics tab
            content_column.controls.append(ft.Text("Statistics Content"))
        case 3:
            # Create Project tab (only available to 'admin' and 'manager')
            if user_role == 'operator':
                show_access_denied_dialog("Access Denied: You do not have access to projects")
            else:
                db_manager_tabs = db_management_tab_menu(user_role)
                content_column.controls.append(db_manager_tabs)
        case 4:
            # Search tab
            content_column.controls.append(ft.Text("Search Content"))
        case 5:
            # Settings tab (only available to 'admin')
            if user_role not in ['admin', 'super_user']:
                show_access_denied_dialog("Access Denied: You do not have access to settings")
            else:
                settings_elements(content_column, page)
        case 6:
            # Exit the application
            page.window_close()

    # Update the content column with the new content
    content_column.update()
    page.update()
