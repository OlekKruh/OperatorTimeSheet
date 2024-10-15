import flet as ft
from DataBase.crud import create_record
from DataBase.db_engine import load_db_settings


save_button = ft.FilledButton(
    text='Save',
    on_click=lambda e: create_record(),
    style=ft.ButtonStyle(
        color=ft.colors.BLACK,
        bgcolor=ft.colors.WHITE,

    )
)
