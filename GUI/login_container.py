import flet as ft
from .home_screen import home_screen
from .constants import *


def login_elements(page: ft.Page):
    """
    Creates and displays the login elements on the page, handling the login process
    and validation. If the login is successful, it navigates to the home screen.

    Args:
        page (ft.Page): The page object where the login elements will be rendered.
    """

    page.clean()

    # Create input fields for the username and password with specified styles
    username_input = ft.TextField(label="Username", width=300, color="white")
    password_input = ft.TextField(label="Password", width=300, password=True, color="white")

    def check_login(e):
        """
        Validates the entered username and password. If correct, it navigates to the home screen.
        Otherwise, it displays an error message.

        Args:
            e (Event): The event that triggered the login validation (usually button click).
        """

        # Clear any existing error messages
        error_message.value = ""
        page.update()

        if username_input.value == SUPER_USER and password_input.value == SUPER_USER_PASSWORD:
            home_screen(page)
        else:
            error_message.value = "Invalid username or password"
        page.update()

    # Login button, which triggers the check_login function
    login_button = ft.ElevatedButton(text="Login", on_click=check_login,
                                     width=100, bgcolor=WIGHT, color=ROJAL_MARIN)

    # Cancel button, which closes the window when clicked
    cancel_button = ft.ElevatedButton(text="Exit", on_click=lambda _: page.window_close(),
                                      width=100, bgcolor=WIGHT, color=ROJAL_MARIN)

    # Text element to display error messages, initially empty
    error_message = ft.Text(value="", color=RED, size=12)

    # Arrange the input fields and buttons in a column, centered on the page
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

    # Add the input fields and buttons to the page, centered in a container
    page.add(
        ft.Container(
            content=column,
            alignment=ft.alignment.center,
            expand=True
        )
    )

    # Add the error message container below the login elements
    page.add(
        ft.Container(
            content=error_message,
            alignment=ft.alignment.center,
            expand=False
        )
    )

    page.update()
