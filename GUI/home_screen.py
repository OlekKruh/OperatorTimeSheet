import flet as ft
from .home_container import home_elements
from .constants import *


def home_screen(page: ft.Page):

    #page.window_maximized = True
    page.window_title_bar_hidden = False
    page.title = APP_TITLE
    page.bgcolor = WIGHT

    page.window_min_width = 1280
    page.window_min_height = 800

    home_elements(page)

    page.update()
