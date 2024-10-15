import flet as ft
import bcrypt


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


def control_prepare_user_dict(page, access_login_field, password_field, repeat_password_field):
    if password_field.value.strip() != repeat_password_field.value.strip():
        show_alert_dialog(page=page, message='Passwords do not match!')
        return None

    hashed_password = hash_password(password_field.value.strip())
    form_data = {
        "access_login": str(access_login_field.value.strip()),
        "password": hashed_password,
    }

    return form_data
