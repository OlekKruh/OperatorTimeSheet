import flet as ft
from .constants import *
from .history_container import history_elements
from .settings_container import settings_elements


def home_elements(page: ft.Page):
    page.clean()

    content_column = ft.Column()

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

    history_elements(content_column)

    page.update()


def on_rail_change(e, content_column, page):
    selected_index = e.control.selected_index

    content_column.controls.clear()

    match selected_index:
        case 0:
            history_elements(content_column)
        case 1:
            content_column.controls.append(ft.Text("Это вкладка Input"))
            #input_elements(content_column)
        case 2:
            content_column.controls.append(ft.Text("Это вкладка Statistics"))
            #statistics_elements(content_column)
        case 3:
            content_column.controls.append(ft.Text("Это вкладка Create Project"))
            #create_project_elements(content_column)
        case 4:
            content_column.controls.append(ft.Text("Это вкладка Search"))
            #search_elements(content_column)
        case 5:
            content_column.controls.append(ft.Text("Это вкладка Setting"))
            settings_elements(content_column, page)
        case 6:
            page.window_close()

    content_column.update()
