import flet as ft
import bcrypt
from icecream import ic


def hash_password(password):
    salt = bcrypt.gensalt(rounds=10)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def show_alert_dialog(page, message):
    alert = ft.AlertDialog(
        title=ft.Text("Warning"),
        content=ft.Text(message),
        actions=[
            ft.TextButton("OK", on_click=lambda e: page.close(alert))
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    page.dialog = alert
    alert.open = True
    page.update()


def validate_order_form(**form_data):
    pass


def validate_enclosure_form(**form_data):
    pass


def validate_company_form(**form_data):
    pass


def validate_operator_form(**form_data):
    pass


def validate_machine_form(**form_data):
    pass


def validate_user_form(page, fields_dict):
    """Валидация формы пользователя. Работаем с готовым словарём."""

    # Получаем значения полей
    access_login = fields_dict.get('Access Login')
    password = fields_dict.get('Password')
    repeat_password = fields_dict.get('Repeat Password')

    # Валидация полей с отображением алертов
    if not access_login:
        show_alert_dialog(page, "Access login is required")
        return
    if not password:
        show_alert_dialog(page, "Password is required")
        return
    if password != repeat_password:
        show_alert_dialog(page, "Passwords do not match")
        return

    # Хешируем пароль
    hashed_password = hash_password(password)

    # Возвращаем валидные данные
    return {
        'access_login': access_login,
        'password': hashed_password
    }





