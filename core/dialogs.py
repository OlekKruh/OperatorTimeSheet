import flet as ft


def show_alert_dialog(page, message):
    alert = ft.AlertDialog(
        title=ft.Text("Warning"),
        content=ft.Text(message),
        actions=[ft.TextButton("OK", on_click=lambda e: page.close(alert))],
        actions_alignment=ft.MainAxisAlignment.END
    )
    page.dialog = alert
    alert.open = True
    page.update()


def show_communication_dialog(event, record):
    dialog = ft.AlertDialog(
        title=ft.Text("Детали записи"),
        content=ft.Text(f"Выбрана строка с данными: {record}"),
        actions=[ft.TextButton("Закрыть", on_click=lambda e: event.page.close(dialog))]
    )
    event.page.dialog = dialog
    dialog.open = True
    event.page.update()
