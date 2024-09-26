import flet as ft
from .constants import *
from DataBase.db_engine import check_database, create_database, test_db_connection, save_db_settings, load_db_settings
import socketserver


with socketserver.TCPServer(("localhost", 0), None) as s:
    free_port = s.server_address[1]

check_result_masege = ft.Text("")

db_settings = load_db_settings()

if isinstance(db_settings, dict):
    host_value = db_settings.get('host')
    port_value = db_settings.get('port')
    user_value = db_settings.get('user')
    password_value = db_settings.get('password')
    dbname_value = db_settings.get('dbname')
else:
    host_value = 'localhost'
    port_value = f'{free_port}'
    user_value = 'User'
    password_value = '12345'
    dbname_value = 'Kradex_Ploter_TimeSheet_db'


def handle_request(request_function, page, host, port, user, password, dbname):
    result = request_function(host, port, user, password, dbname)

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

    host = ft.TextField(label="Host", color=WIGHT, value=host_value,
                        border_color=WIGHT, width=TEXT_WIDTH, )
    port = ft.TextField(label="Port", color=WIGHT, value=port_value,
                        border_color=WIGHT, width=TEXT_WIDTH, )
    user = ft.TextField(label="User", color=WIGHT, value=user_value,
                        border_color=WIGHT, width=TEXT_WIDTH, )
    password = ft.TextField(label="Password", color=WIGHT, value=password_value,
                            password=True, can_reveal_password=True,
                            border_color=WIGHT, width=TEXT_WIDTH, )
    dbname = ft.TextField(label="Database", color=WIGHT, value=dbname_value,
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

    buton_check_database = ft.FilledButton(text="Check for database",
                                           on_click=lambda e:
                                           handle_request(check_database, page,
                                                          host.value,
                                                          port.value,
                                                          user.value,
                                                          password.value,
                                                          dbname.value))
    buton_create_database = ft.FilledButton(text="Create database",
                                            on_click=lambda e:
                                            handle_request(create_database, page,
                                                           host.value,
                                                           port.value,
                                                           user.value,
                                                           password.value,
                                                           dbname.value))
    buton_test_connection = ft.FilledButton(text="Test DB connection",
                                            on_click=lambda e:
                                            handle_request(test_db_connection, page,
                                                           host.value,
                                                           port.value,
                                                           user.value,
                                                           password.value,
                                                           dbname.value))
    save_settings = ft.FilledButton(text="Save",
                                    on_click=lambda e:
                                    handle_request(save_db_settings, page,
                                                   host.value,
                                                   port.value,
                                                   user.value,
                                                   password.value,
                                                   dbname.value))

    buttons_container = ft.Container(
        ft.Row(
            [
                buton_check_database,
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
