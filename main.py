import flet as ft
from flet_core import TextAlign

from GUI.login_screen import login_screen
from DataBase.db_engine import load_db_settings


def main(page: ft.Page):

    dialog = ft.AlertDialog(
        content=ft.Text("Failed to load database settings.\n"
                        "Only superuser can log in.",
                        color="red",
                        size=14,
                        text_align=TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD),
        modal=True,
        actions=[
            ft.TextButton("Continue", on_click=lambda e: page.close(dialog))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    db_settings = load_db_settings()

    if isinstance(db_settings, dict):
        login_screen(page)  # Call login screen
    else:
        page.dialog = dialog
        dialog.open = True
        login_screen(page)
        page.update()


ft.app(target=main)  # Start app
