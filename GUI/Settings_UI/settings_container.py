import flet as ft
from GUI.constants import *
from DataBase.db_engine import create_database, test_db_connection, save_db_settings, load_db_settings #delete_database

# A message placeholder for displaying the result of operations
check_result_masege = ft.Text("")

# Load database settings from file
db_settings = load_db_settings()

# If loading settings failed (not a dict), assign default settings
if not isinstance(db_settings, dict):
    db_settings = {
        'host': 'localhost',
        'port': '5432',
        'user': 'User',
        'password': '12345',
        'dbname': 'Noname_db',
    }


def handle_request(request_function, page):
    """
    Handles database-related requests by executing the provided function and displaying the result in a dialog.

    Args:
        request_function (callable): The function to execute (e.g., creating the database, testing connection).
        page (ft. Page): The page on which to display the result dialog.
    """

    # Execute the provided function with db_settings and get the result
    result = request_function()

    # Create an alert dialog to show the result of the request
    dialog = ft.AlertDialog(
        content=ft.Text(result),
        modal=True,
        actions=[
            ft.TextButton("Continue", on_click=lambda e: page.close(dialog))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    # Assign the dialog to the page and open it
    page.dialog = dialog
    dialog.open = True
    page.update()


def settings_elements(content_column: ft.Column, page: ft.Page):
    """
    Generates and displays the UI elements for configuring the database connection settings.

    Args:
        content_column (ft.Column): The column where all the UI elements will be added.
        page (ft.Page): The page on which the elements are displayed.
    """

    # Clear the current content
    content_column.controls.clear()

    # Header text for the database settings section
    header = ft.Container(
        content=ft.Text("DataBase location", size=16, color=ft.colors.WHITE),
        padding=ft.padding.all(20),
        alignment=ft.alignment.center_left,
    )

    # Text fields for database settings with default or loaded values
    host = ft.TextField(label="Host", color=ft.colors.WHITE, value=db_settings.get('host'),
                        border_color=ft.colors.WHITE, width=TEXT_WIDTH, )
    port = ft.TextField(label="Port", color=ft.colors.WHITE, value=db_settings.get('port'),
                        border_color=ft.colors.WHITE, width=TEXT_WIDTH, )
    user = ft.TextField(label="User", color=ft.colors.WHITE, value=db_settings.get('user'),
                        border_color=ft.colors.WHITE, width=TEXT_WIDTH, )
    password = ft.TextField(label="Password", color=ft.colors.WHITE, value=db_settings.get('password'),
                            password=True, can_reveal_password=True,
                            border_color=ft.colors.WHITE, width=TEXT_WIDTH, )
    dbname = ft.TextField(label="Database", color=ft.colors.WHITE, value=db_settings.get('dbname'),
                          border_color=ft.colors.WHITE, width=TEXT_WIDTH, )

    # Container for the text fields
    textfield_container = ft.Container(
        ft.Column(
            [
                host,
                port,
                user,
                password,
                dbname,
            ],
        ),
        margin=ft.margin.only(left=20),
    )

    # Function to handle the saving of settings
    def save_settings_event(e):
        """
        Event handler to save database settings entered by the user.

        Args:
            e (Event): The event that triggered this function.
        """

        # Update the db_settings dictionary with the values from the text fields
        db_settings['host'] = host.value
        db_settings['port'] = port.value
        db_settings['user'] = user.value
        db_settings['password'] = password.value
        db_settings['dbname'] = dbname.value

        # Call the handle_request function to save the settings
        handle_request(lambda: save_db_settings(db_settings), page)

    # Button to create the database
    buton_create_database = ft.FilledButton(
        text="Create database",
        on_click=lambda e: handle_request(create_database, page)
    )

    # Button to test the database connection
    buton_test_connection = ft.FilledButton(
        text="Test DB connection",
        on_click=lambda e: handle_request(test_db_connection, page)
    )

    # Button to delete the database
    # buton_delete_database = ft.FilledButton(
    #     text="Delete database",
    #     on_click=lambda e: handle_request(delete_database, page)
    # )

    # Button to save the database settings
    save_settings = ft.FilledButton(text="Save", on_click=save_settings_event)

    # Container for the buttons (create, test connection, and save)
    buttons_container = ft.Container(
        ft.Row(
            [
                buton_create_database,
                buton_test_connection,
                save_settings,
                # buton_delete_database,
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        margin=ft.margin.only(left=20),
    )

    # Main content container that holds the header, text fields, and buttons
    content_container = ft.Container(
        content=ft.Column(
            [
                header,
                textfield_container,
                buttons_container,
            ],
            spacing=10,
        ),
        alignment=ft.alignment.top_left,
    )

    # Add the content container to the column and update the display
    content_column.controls.append(content_container)
    content_column.update()
