import flet as ft
from core.Login.login_container import login_elements
from core.constants import *


def login_screen(page: ft.Page):
    """
    Sets up and displays the login screen for the application.

    Args:
        page (ft.Page): The page object where the login screen will be rendered.
    """

    page.window_maximized = True
    page.window_title_bar_hidden = True
    page.title = APP_TITLE
    page.bgcolor = ROJAL_MARIN

    login_elements(page)

    page.update()
