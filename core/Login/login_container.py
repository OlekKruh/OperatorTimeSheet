import flet as ft
from core.constants import *
from .login_handler import check_login  # Импортируем логику из login_logic.py


def login_elements(page: ft.Page):
    page.clean()

    # Создаем поля ввода для логина и пароля
    username_input = ft.TextField(label="Username", width=300, color="white")
    password_input = ft.TextField(label="Password", width=300, password=True, color="white")

    password_input.on_submit = lambda e: check_login(page, username_input, password_input)

    # Кнопка для входа, которая вызывает check_login
    login_button = ft.ElevatedButton(
        text="Login",
        on_click=lambda e: check_login(page, username_input, password_input),
        width=100, bgcolor=ft.colors.WHITE, color=ROJAL_MARIN
    )

    # Кнопка для выхода
    cancel_button = ft.ElevatedButton(
        text="Exit",
        on_click=lambda _: page.window_close(),
        width=100, bgcolor=ft.colors.WHITE, color=ROJAL_MARIN
    )

    # Размещаем элементы в колонке
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

    # Добавляем элементы на страницу
    page.add(
        ft.Container(
            content=column,
            alignment=ft.alignment.center,
            expand=True
        )
    )

    page.update()
