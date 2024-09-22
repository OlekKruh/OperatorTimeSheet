import flet as ft
from .home_elements import home_elements
from .constants import *


def home_screen(page: ft.Page):

    page.window_maximized = True
    page.window_title_bar_hidden = True
    page.title = APP_TITLE
    page.bgcolor = WIGHT

    home_elements(page)

    page.update()
