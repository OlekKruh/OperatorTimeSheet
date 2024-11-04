import flet as ft
from DataBase.db_engine import get_db_session
from DataBase.models import get_pretty_name
from .expansion_tiles_for_tab_menu import expansion_tiles


def create_tab(label, icon, allow_create=True):
    """
    Создаёт вкладку для DB Manager.

    Args:
        label (str): Название вкладки.
        icon (IconData): Иконка для вкладки.
        allow_create (bool): Флаг, позволяющий добавление create_expansion_tile.

    Returns:
        ft.Tab: Сконфигурированная вкладка.
    """
    pretty_label = get_pretty_name(label)

    with get_db_session() as session:
        expansion_tile_create = expansion_tiles(label, mode='create') if allow_create else None
        expansion_tile_delete_update = expansion_tiles(label, mode='delete_update')

        controls = []
        if expansion_tile_create:
            controls.append(expansion_tile_create)
        controls.append(expansion_tile_delete_update)

        return ft.Tab(
            text=pretty_label,
            content=ft.Container(
                ft.Column(
                    controls=controls,
                    scroll=ft.ScrollMode.ALWAYS
                ),
                padding=20,
                animate_opacity=900,
            ),
            icon=icon
        )


def db_management_tab_menu(user_role: str):
    """
    Создаёт меню вкладок для управления базой данных.
    Вкладки 'Users' и 'ChangeLog' видны только для пользователей с ролями 'admin' или 'superuser'.

    Args:
        user_role: Роль вошедшего пользователя ('admin', 'superuser', 'manager', 'operator').

    Returns:
        ft.Tabs: Компонент вкладок Flet с соответствующими вкладками.
    """
    # Общие вкладки, доступные всем пользователям
    tabs = [
        create_tab('time_sheet', ft.icons.TABLE_ROWS_ROUNDED, allow_create=False),
        create_tab('order', ft.icons.BORDER_COLOR),
        create_tab('enclosure', ft.icons.ALL_INBOX),
        create_tab('company', ft.icons.HOME_WORK_SHARP),
        create_tab('operator', ft.icons.PEOPLE_SHARP),
        create_tab('machine', ft.icons.DRAW)
    ]

    # Добавляем вкладки 'Users' и 'ChangeLog' только для администраторов и суперпользователей
    if user_role in ['admin', 'super_user']:
        tabs.append(create_tab('users', ft.icons.PERSON))
        tabs.append(create_tab('change_log', ft.icons.HISTORY, allow_create=False))

    # Возвращаем компонент Tabs с улучшенной анимацией для плавного перехода
    return ft.Tabs(
        selected_index=0,
        animation_duration=900,  # Увеличена длительность анимации до 900 мс для плавности
        tabs=tabs,
        expand=True,
        indicator_color=ft.colors.GREEN_ACCENT_400,
        divider_color=ft.colors.WHITE,
        label_color=ft.colors.GREEN_ACCENT_400,
    )
