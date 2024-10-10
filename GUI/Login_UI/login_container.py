import flet as ft
from GUI.Home_UI.home_screen import home_screen
from GUI.constants import *
import bcrypt
from sqlalchemy.orm import Session
from DataBase.db_engine import get_engine, load_db_settings
from DataBase.models import Users


def login_elements(page: ft.Page):
    """
    Creates and displays the login elements on the page, handling the login process
    and validation. If the login is successful, it navigates to the home screen with the appropriate user role.

    Args:
        page (ft.Page): The page object where the login elements will be rendered.
    """

    page.clean()

    # Create input fields for the username and password with specified styles.
    username_input = ft.TextField(label="Username", width=300, color="white")
    password_input = ft.TextField(label="Password", width=300, password=True, color="white")

    def check_login(e):
        """
        Validates the entered username and password. If correct, it navigates to the home screen with the correct role.
        Otherwise, it displays an error message.

        Args:
            e (Event): The event that triggered the login validation (usually button click).
        """

        # Clear any existing error messages
        error_message.value = ""
        page.update()

        username = username_input.value
        password = password_input.value.encode('utf-8')

        if username == SUPER_USER:
            # Hardcoded superuser check
            if bcrypt.checkpw(password, SUPER_USER_PASS_HASH.encode('utf-8')):
                user_role = 'super_user'  # Hardcoded role for the superuser
                home_screen(page, user_role)
            else:
                error_message.value = "Invalid superuser password"
        else:
            # Load the DB settings from the JSON file
            db_connection_settings = load_db_settings()

            if isinstance(db_connection_settings, str):
                error_message.value = db_connection_settings
            else:
                # Get the engine and session using your custom functions
                engine = get_engine(db_connection_settings)
                session = Session(engine)

                try:
                    # Fetch the user by username (access_login)
                    user = session.query(Users).filter(Users.access_login.like(username)).first()

                    if user:
                        # Verify the hashed password using bcrypt
                        if bcrypt.checkpw(password, user.hash_pass.encode('utf-8')):
                            user_role = str(user.access_login)  # Expected type 'str', 'InstrumentedAttribute' instead
                            home_screen(page, user_role)

                        else:
                            error_message.value = "Invalid username or password"
                    else:
                        error_message.value = "User not found"
                except Exception as db_error:
                    error_message.value = f"Database error: {db_error}"
                finally:
                    session.close()

        page.update()

    # Assign the check_login function to handle the "Enter" key press
    #username_input.on_submit = check_login
    password_input.on_submit = check_login

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
