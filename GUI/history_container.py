import flet as ft
from .constants import *


def history_elements(content_column: ft.Column):
    # Очищаем колонку перед добавлением новых элементов
    content_column.controls.clear()

    # Названия колонок
    columns = [
        "Date", "Operator", "Start", "Company", "Case", "Variant", "On\nOrder",
        "Processing\nSide", "Quantity\nDone", "Notes\nDescription", "Machine",
        "End", "Work\n[Minutes]"
    ]

    # Создаем заголовки колонок
    headers = [ft.DataColumn(ft.Text(col, text_align=ft.TextAlign.CENTER)) for col in columns]

    # Создаем таблицу
    data_table = ft.DataTable(
        columns=headers,
        rows=[],  # Здесь должны быть ваши строки с данными
        column_spacing=10,
        data_text_style=ft.TextStyle(size=12),
        border=ft.border.all(1, WIGHT),
        border_radius=10,
        vertical_lines=ft.BorderSide(1, WIGHT),
    )

    # Добавляем таблицу в ListView для возможности прокрутки
    scroll_container = ft.Container(
        content=ft.ListView(
            controls=[data_table],  # Список элементов для отображения
            auto_scroll=True,  # Автопрокрутка
        ),
        expand=True
    )

    # Добавляем контейнер с таблицей в переданную колонку
    content_column.controls.append(scroll_container)

    # Обновляем колонку после добавления контента
    content_column.update()