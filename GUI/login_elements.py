import flet as ft
from .home_screen import home_screen
from .constants import *


def login_elements(page: ft.Page):
    page.clean()

    # Input fields
    username_input = ft.TextField(label="Username", width=300, color="white")
    password_input = ft.TextField(label="Password", width=300, password=True, color="white")

    # Функция проверки логина и пароля
    def check_login(e):
        error_message.value = ""
        page.update()

        if username_input.value == test_username and password_input.value == test_password:
            home_screen(page)
        else:
            error_message.value = "Invalid username or password"
        page.update()

    # Buttons
    login_button = ft.ElevatedButton(text="Login", on_click=check_login,
                                     width=100, bgcolor=WIGHT, color=ROJAL_MARIN)
    cancel_button = ft.ElevatedButton(text="Exit", on_click=lambda _: page.window_close(),
                                      width=100, bgcolor=WIGHT, color=ROJAL_MARIN)

    # Error message
    error_message = ft.Text(value="", color=RED, size=12)

    # Elements layout
    # Container with column elements
    column = ft.Column(
        controls=[
            username_input,
            password_input,
            login_button,
            cancel_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    # Container centr-centr layout
    page.add(
        ft.Container(
            content=column,
            alignment=ft.alignment.center,
            expand=True
        )
    )

    # Error message botom-centr layout
    page.add(
        ft.Container(
            content=error_message,
            alignment=ft.alignment.center,
            expand=False
        )
    )

    page.update()
