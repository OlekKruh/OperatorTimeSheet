import flet as ft
from .constants import *
from DataBase.db_engine import check_database
import socketserver

with socketserver.TCPServer(("localhost", 0), None) as s:
    free_port = s.server_address[1]

check_result_masege = ft.Text("")


def check_database_request():
    result = check_database()
    check_result_masege.value = result
    check_result_masege.update()


def create_database_request():
    pass


def test_db_connection_request():
    pass


def seve_request():
    pass


def settings_elements(content_column: ft.Column):
    content_column.controls.clear()

    header = ft.Container(
        content=ft.Text("DataBase location", size=16, color=WIGHT),
        padding=ft.padding.all(20),
        alignment=ft.alignment.center_left,
    )

    ip = ft.TextField(label="IP", color=WIGHT,
                      border_color=WIGHT, width=text_width, )
    host = ft.TextField(label="Host", color=WIGHT, value='localhost',
                        border_color=WIGHT, width=text_width, )
    port = ft.TextField(label="Port", color=WIGHT, value=f'{free_port}',
                        border_color=WIGHT, width=text_width, )
    user = ft.TextField(label="User", color=WIGHT, value='User',
                        border_color=WIGHT, width=text_width, )
    password = ft.TextField(label="Password", color=WIGHT, value='12345', password=True, can_reveal_password=True,
                            border_color=WIGHT, width=text_width, )
    dbname = ft.TextField(label="Database", color=WIGHT, value='Kradex_Ploter_TimeSheet_db',
                          border_color=WIGHT, width=text_width, )

    textfield_container = ft.Container(
        ft.Column(
            [
                ip,
                host,
                port,
                user,
                password,
                dbname,
            ],
        ),
        margin=ft.margin.only(left=20),
    )

    buton_check_database = ft.FilledButton(text="Check for database", on_click=lambda e: check_database_request())
    buton_create_database = ft.FilledButton(text="Create database", on_click=lambda e: create_database_request())
    buton_test_connection = ft.FilledButton(text="Test DB connection", on_click=lambda e: test_db_connection_request())
    save_settings = ft.FilledButton(text="Save", on_click=lambda e: seve_request())

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
