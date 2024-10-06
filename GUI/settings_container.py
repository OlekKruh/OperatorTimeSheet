import flet as ft
from .constants import *
from DataBase.db_engine import create_database, test_db_connection, save_db_settings, load_db_settings

check_result_masege = ft.Text("")

db_settings = load_db_settings()

if not isinstance(db_settings, dict):
    db_settings = {
        'host': 'localhost',
        'port': '5432',
        'user': 'User',
        'password': '12345',
        'dbname': 'Noname_db',
    }


def handle_request(request_function, page, db_settings):
    result = request_function(db_settings)

    dialog = ft.AlertDialog(
        content=ft.Text(result),
        modal=True,
        actions=[
            ft.TextButton("Continue", on_click=lambda e: page.close(dialog))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    page.dialog = dialog
    dialog.open = True
    page.update()


def settings_elements(content_column: ft.Column, page: ft.Page):
    content_column.controls.clear()

    header = ft.Container(
        content=ft.Text("DataBase location", size=16, color=WIGHT),
        padding=ft.padding.all(20),
        alignment=ft.alignment.center_left,
    )

    host = ft.TextField(label="Host", color=WIGHT, value=db_settings.get('host'),
                        border_color=WIGHT, width=TEXT_WIDTH, )
    port = ft.TextField(label="Port", color=WIGHT, value=db_settings.get('port'),
                        border_color=WIGHT, width=TEXT_WIDTH, )
    user = ft.TextField(label="User", color=WIGHT, value=db_settings.get('user'),
                        border_color=WIGHT, width=TEXT_WIDTH, )
    password = ft.TextField(label="Password", color=WIGHT, value=db_settings.get('password'),
                            password=True, can_reveal_password=True,
                            border_color=WIGHT, width=TEXT_WIDTH, )
    dbname = ft.TextField(label="Database", color=WIGHT, value=db_settings.get('dbname'),
                          border_color=WIGHT, width=TEXT_WIDTH, )

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

    def save_settings_event(e):
        db_settings['host'] = host.value
        db_settings['port'] = port.value
        db_settings['user'] = user.value
        db_settings['password'] = password.value
        db_settings['dbname'] = dbname.value
        handle_request(save_db_settings, page, db_settings)

    buton_create_database = ft.FilledButton(text="Create database",
                                            on_click=lambda e:
                                            handle_request(create_database, page,
                                                           db_settings))
    buton_test_connection = ft.FilledButton(text="Test DB connection",
                                            on_click=lambda e:
                                            handle_request(test_db_connection, page,
                                                           db_settings))
    save_settings = ft.FilledButton(text="Save",
                                    on_click=save_settings_event)

    buttons_container = ft.Container(
        ft.Row(
            [
                buton_create_database,
                buton_test_connection,
                save_settings,
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        margin=ft.margin.only(left=20),
    )

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

    content_column.controls.append(content_container)

    content_column.update()
