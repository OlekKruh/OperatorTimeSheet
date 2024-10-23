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