import flet as ft
from .home_navigation_rail import home_elements
from .constants import *


def home_screen(page: ft.Page):
    """
    Sets up and displays the home screen for the application. Configures window settings
    such as minimum size, title and background color, and loads the home screen elements.

    Args:
        page (ft. Page): The page object where the home screen will be rendered.
    """

    # Configure window settings
    # page.window_maximized = True # Uncomment in end
    # page.window_title_bar_hidden = True # Uncomment in end
    page.window_title_bar_hidden = False  # Coment in end
    page.title = APP_TITLE
    page.bgcolor = WIGHT

    # Minimum dimensions of the window to ensure proper display
    page.window_min_width = 1280
    page.window_min_height = 800

    # Load and display the home screen elements
    home_elements(page)

    page.update()
