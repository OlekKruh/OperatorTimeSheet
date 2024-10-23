import flet as ft
from flet_core import TextAlign
from core.Home.home_screen import home_screen
from DataBase.db_engine import load_db_settings
from DataBase.event_listener import register_listeners
from core.Login.login_screen import login_screen
from DataBase.session_manager import set_user_session

register_listeners()


def main(page: ft.Page):
    dialog = ft.AlertDialog(
        content=ft.Text("Failed to load database settings.\n"
                        "Please contact the system administrator.",
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
        set_user_session(user_id=0, user_role='super_user')
        home_screen(page, user_role='super_user')
        #login_screen(page)
    else:
        page.dialog = dialog
        dialog.open = True
        set_user_session(user_id=0, user_role='super_user')
        home_screen(page, user_role='super_user')
        #login_screen(page)
        page.update()


ft.app(target=main)  # Start app
