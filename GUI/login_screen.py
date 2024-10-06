import flet as ft
from .login_container import login_elements
from .constants import *


def login_screen(page: ft.Page):

    # Centering the window
    page.window_width = LOGIN_WINDOW_WIDTH
    page.window_height = LOGIN_WINDOW_HEIGHT
    page.window_center()

    # Login window settings
    page.window_title_bar_hidden = True
    page.title = APP_TITLE
    page.bgcolor = ROJAL_MARIN

    login_elements(page)

    page.update()
