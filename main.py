import asyncio
import flet as ft
from flet_core import TextAlign
from DataBase.cache_manager import initialize_cache, poll_change_log
from core.Home.home_screen import home_screen
from DataBase.db_engine import load_db_settings
from DataBase.event_listener import register_listeners
from core.Login.login_screen import login_screen
from DataBase.session_manager import set_user_session

register_listeners()


async def main(page: ft.Page):
    # Инициализируем кеш при запуске
    initialize_cache()

    # Запускаем параллельно задачу опроса ChangeLog
    asyncio.create_task(poll_change_log())

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
        # login_screen(page)
    else:
        page.dialog = dialog
        dialog.open = True
        set_user_session(user_id=0, user_role='super_user')
        home_screen(page, user_role='super_user')
        # login_screen(page)
        page.update()


# Запуск с помощью asyncio.run
asyncio.run(ft.app_async(target=main))
