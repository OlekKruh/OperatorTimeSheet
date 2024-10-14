import flet as ft
from GUI.Home_UI.home_navigation_rail import home_elements
from GUI.constants import *


def home_screen(page: ft.Page, user_role: str):
    """
    Sets up and displays the home screen for the application. Configures window settings
    such as minimum size, title and background color, and loads the home screen elements.

    Args:
        page (ft. Page): The page object where the home screen will be rendered.
        user_role (str): Role of the logged-in user ('admin', 'manager', 'operator').
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
