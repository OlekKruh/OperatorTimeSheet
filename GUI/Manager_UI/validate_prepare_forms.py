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


def validate_order_form(page, fields_dict):
    pass


def validate_enclosure_form(page, fields_dict):
    sap_id = fields_dict.get('Sap Id')
    enclosure_title = fields_dict.get('Enclosure full Title')
    base = fields_dict.get('Base')
    cover = fields_dict.get('Cover')
    filter_ = fields_dict.get('Filter')
    pcb = fields_dict.get('PCB mounting plate')
    panel = fields_dict.get('Panel')
    slot_mask = fields_dict.get('Slot Mask')

    # Validation checks
    if not sap_id:
        show_alert_dialog(page, "Sap ID must be provided")
        return
    if not enclosure_title:
        show_alert_dialog(page, "Enclosure full Title must be provided")
        return
    if not any([base, cover, pcb, slot_mask, panel]):
        show_alert_dialog(page, "At least one part of the enclosure must be selected")
        return

    return {
        'sap_id': sap_id,
        'enclosure_title': enclosure_title,
        'base': int(base),
        'cover': int(cover),
        'filter': int(filter_),
        'pcb': int(pcb),
        'panel': int(panel),
        'slot_mask': int(slot_mask)
    }


def validate_company_form(page, fields_dict):
    sap_id = fields_dict.get('Sap Id')
    company_title = fields_dict.get('Company title')
    company_country = fields_dict.get('Company HQ country')
    company_shipping_address = fields_dict.get('Company shipping address')
    company_phone = fields_dict.get('Company phone number')
    company_email = fields_dict.get('Company email')

    if not sap_id:
        show_alert_dialog(page, "Sap ID must be provided")
        return
    if not company_title:
        show_alert_dialog(page, "Company title must be provided")
        return
    if not company_country:
        show_alert_dialog(page, "Company country must be provided")
        return
    if not company_shipping_address:
        show_alert_dialog(page, "Company shipping address must be provided")
        return
    if not company_phone:
        show_alert_dialog(page, "Company phone number must be provided")
        return
    if not company_email:
        show_alert_dialog(page, "Company email must be provided")
        return

    return {
        'sap_id': sap_id,
        'company_title': company_title,
        'company_country': company_country,
        'company_shipping_address': company_shipping_address,
        'company_phone': company_phone,
        'company_email': company_email
    }


def validate_operator_form(page, fields_dict):
    operator_name = fields_dict.get('Operator Name')
    skill = fields_dict.get('Operator skill level')
    # contact_phone = fields_dict.get('Operator contact phone')

    if not operator_name:
        show_alert_dialog(page, "Operator Name is required.")
        return
    if not skill:
        show_alert_dialog(page, "Operator skill level is required.")
        return
    # if not contact_phone:
    #     show_alert_dialog(page, "Operator contact phone is required.")
    #     return

    return {
        'operator_name': operator_name,
        'skill': skill,
        # 'contact_phone': contact_phone
    }


def validate_machine_form(page, fields_dict):
    sap_id = fields_dict.get('Sap Id')
    machine_title = fields_dict.get('Machine title')
    machine_serial_number = fields_dict.get('Machine serial number')
    machine_manufacturer = fields_dict.get('Machine manufacturer')
    machine_year_production = fields_dict.get('Machine year production')

    if not sap_id:
        show_alert_dialog(page, "Sap id is required.")
        return
    if not machine_title:
        show_alert_dialog(page, "Machine title is required.")
        return
    if not machine_serial_number:
        show_alert_dialog(page, "Machine serial number is required.")
        return
    if not machine_manufacturer:
        show_alert_dialog(page, "Machine manufacturer is required.")
        return
    if not machine_year_production:
        show_alert_dialog(page, "Machine year production is required.")
        return

    # Преобразуем "machine_year_production" в формат "YYYY-MM-DD"
    try:
        machine_year_production = f"{int(machine_year_production)}-01-01"  # Пример: '2000' -> '2000-01-01'
    except ValueError:
        show_alert_dialog(page, "Invalid year format. Must be 'YYYY'")
        return

    return {
        'sap_id': sap_id,
        'machine_title': machine_title,
        'machine_serial_number': machine_serial_number,
        'machine_manufacturer': machine_manufacturer,
        'machine_year_production': machine_year_production
    }


def validate_user_form(page, fields_dict):
    access_login = fields_dict.get('Access Login')
    password = fields_dict.get('Password')
    repeat_password = fields_dict.get('Repeat Password')

    if not access_login:
        show_alert_dialog(page, "Access login is required")
        return
    if not password:
        show_alert_dialog(page, "Password is required")
        return
    if password != repeat_password:
        show_alert_dialog(page, "Passwords do not match")
        return

    hashed_password = hash_password(password)

    return {
        'access_login': access_login,
        'hash_pass': hashed_password
    }





