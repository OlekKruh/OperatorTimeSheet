import bcrypt
from sqlalchemy.exc import OperationalError
from DataBase.db_engine import get_db_session
from DataBase.models import Users
from DataBase.session_manager import set_user_session
from core.Home.home_screen import home_screen
from ..dialogs import show_alert_dialog


def check_login(page, username_input, password_input):
    username = username_input.value
    password = password_input.value.encode('utf-8')

    try:
        with get_db_session() as session:
            user = session.query(Users).filter(Users.access_login.like(username)).first()

            if user:
                if bcrypt.checkpw(password, user.hash_pass.encode('utf-8')):
                    user_role = str(user.access_login)
                    user_id = int(user.user_id)

                    set_user_session(user_id, user_role)

                    home_screen(page, user_role)
                else:
                    show_alert_dialog(page, "Invalid username or password")
            else:
                show_alert_dialog(page, "User not found")
    except OperationalError:
        if username == "admin":
            show_alert_dialog(page, "Database not found. You have entered admin mode without a database.")
            set_user_session(user_id=1, user_role="admin")
            home_screen(page, user_role="admin")
        else:
            show_alert_dialog(page, "Database not found. Please contact administration.")
    except Exception as db_error:
        show_alert_dialog(page, f"Database error: {db_error}")

    page.update()
