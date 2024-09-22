import flet as fl
from GUI.login_screen import login_screen


def main(page: fl.Page):
    login_screen(page)  # Call login screen


fl.app(target=main)  # Start app
