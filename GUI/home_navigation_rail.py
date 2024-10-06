import flet as ft
from .constants import *
from .history_container import history_elements
from .settings_container import settings_elements


def home_elements(page: ft.Page):
    """
    Sets up the main Home Screen of the application with a persistent
    Navigation Rail, and a default display of history elements.

    Args:
        page (ft. Page): The Flet page object that will display the home screen.
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
                icon_content=ft.Icon(ft.icons.INPUT),
                selected_icon_content=ft.Icon(ft.icons.INPUT, color=ROJAL_MARIN),
                label_content=ft.Text("Input")
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.INSERT_CHART),
                selected_icon_content=ft.Icon(ft.icons.INSERT_CHART, color=ROJAL_MARIN),
                label_content=ft.Text("Statistics")
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.CREATE),
                selected_icon_content=ft.Icon(ft.icons.CREATE, color=ROJAL_MARIN),
                label_content=ft.Text("Create\nProject")
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
        on_change=lambda e: on_rail_change(e, content_column, page),
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


def on_rail_change(e, content_column, page):
    """
    Handles the logic for updating the content area when a new tab is selected
    in the NavigationRail.

    Args:
        e: Event object containing the selected tab index.
        content_column (ft. Column): The column to display the selected tab's content.
        Page (ft. Page): The Flet page object to allow window control actions like closing.
    """
    selected_index = e.control.selected_index

    # Clear the current content
    content_column.controls.clear()

    # Switch based on the selected index
    match selected_index:
        case 0:
            # History tab
            history_elements(content_column)
        case 1:
            # Input tab
            content_column.controls.append(ft.Text("Input"))
            # input_elements(content_column)
        case 2:
            # Statistics tab
            content_column.controls.append(ft.Text("Statistics"))
            # statistics_elements(content_column)
        case 3:
            # Create Project tab
            content_column.controls.append(ft.Text("Project"))
            # create_project_elements(content_column)
        case 4:
            # Search tab
            content_column.controls.append(ft.Text("Search"))
            # search_elements(content_column)
        case 5:
            # Settings tab
            content_column.controls.append(ft.Text("Setting"))
            settings_elements(content_column, page)
        case 6:
            # Exit the application
            page.window_close()

    # Update the content column with the new content
    content_column.update()
