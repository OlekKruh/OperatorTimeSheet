import flet as ft
from core.Home.home_navigation_rail import home_elements
from core.constants import *


def home_screen(page: ft.Page, user_role: str,):
    """
    Main screen of the application where different tabs are shown depending on user role.

    Args:
        page (Page): The Flet page object.
        user_role (str): The role of the logged-in user.
    """

    # Configure window settings
    page.window_maximized = False
    page.window_title_bar_hidden = False
    page.title = APP_TITLE
    page.bgcolor = ft.colors.WHITE

    # Minimum dimensions of the window to ensure proper display
    page.window_min_width = 1280
    page.window_min_height = 800

    # Load and display the home screen elements
    home_elements(page, user_role)

    page.update()
