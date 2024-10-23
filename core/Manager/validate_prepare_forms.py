import bcrypt
from ..alert_dialog import show_alert_dialog


def hash_password(password):
    salt = bcrypt.gensalt(rounds=10)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def validate_required_fields(page, fields_dict, required_fields):
    """
    Проверяет наличие обязательных полей в fields_dict.

    Args:
        page: Страница Flet для отображения диалога.
        fields_dict: Словарь с данными полей формы.
        required_fields: Список обязательных полей.

    Returns:
        bool: True, если все обязательные поля заполнены, иначе False.
    """
    for field in required_fields:
        if not fields_dict.get(field):
            show_alert_dialog(page, f"{field} is required.")
            return False
    return True


def validate_order_form(page, fields_dict):
    required_fields = ['Company_id', 'Enclosure_id', 'Variant', 'Order quantity', 'Operations quantity']
    if not validate_required_fields(page, fields_dict, required_fields):
        return

    return fields_dict


def validate_enclosure_form(page, fields_dict):
    required_fields = ['Sap Id', 'Enclosure full Title']
    if not validate_required_fields(page, fields_dict, required_fields):
        return

    base = fields_dict.get('Base')
    cover = fields_dict.get('Cover')
    filter_ = fields_dict.get('Filter')
    pcb = fields_dict.get('PCB mounting plate')
    panel = fields_dict.get('Panel')
    slot_mask = fields_dict.get('Slot Mask')

    # Проверка наличия хотя бы одной выбранной части
    if not any([base, cover, pcb, slot_mask, panel]):
        show_alert_dialog(page, "At least one part of the enclosure must be selected")
        return

    return {
        'sap_id': fields_dict.get('Sap Id'),
        'enclosure_title': fields_dict.get('Enclosure full Title'),
        'base': int(base),
        'cover': int(cover),
        'filter': int(filter_),
        'pcb': int(pcb),
        'panel': int(panel),
        'slot_mask': int(slot_mask)
    }


def validate_company_form(page, fields_dict):
    required_fields = [
        'Sap Id', 'Company title', 'Company HQ country',
        'Company shipping address', 'Company phone number', 'Company email'
    ]
    if not validate_required_fields(page, fields_dict, required_fields):
        return

    return {
        'sap_id': fields_dict.get('Sap Id'),
        'company_title': fields_dict.get('Company title'),
        'company_country': fields_dict.get('Company HQ country'),
        'company_shipping_address': fields_dict.get('Company shipping address'),
        'company_phone': fields_dict.get('Company phone number'),
        'company_email': fields_dict.get('Company email')
    }


def validate_operator_form(page, fields_dict):
    required_fields = ['Operator Name', 'Operator skill level']
    if not validate_required_fields(page, fields_dict, required_fields):
        return

    return {
        'operator_name': fields_dict.get('Operator Name'),
        'skill': fields_dict.get('Operator skill level')
    }


def validate_machine_form(page, fields_dict):
    required_fields = [
        'Sap Id', 'Machine title', 'Machine serial number',
        'Machine manufacturer', 'Machine year production'
    ]
    if not validate_required_fields(page, fields_dict, required_fields):
        return

    # Преобразуем "machine_year_production" в формат "YYYY-MM-DD"
    try:
        machine_year_production = f"{int(fields_dict.get('Machine year production'))}-01-01"  # Пример: '2000' -> '2000-01-01'
    except ValueError:
        show_alert_dialog(page, "Invalid year format. Must be 'YYYY'")
        return

    return {
        'sap_id': fields_dict.get('Sap Id'),
        'machine_title': fields_dict.get('Machine title'),
        'machine_serial_number': fields_dict.get('Machine serial number'),
        'machine_manufacturer': fields_dict.get('Machine manufacturer'),
        'machine_year_production': machine_year_production
    }


def validate_user_form(page, fields_dict):
    required_fields = ['Access Login', 'Password', 'Repeat Password']
    if not validate_required_fields(page, fields_dict, required_fields):
        return

    password = fields_dict.get('Password')
    repeat_password = fields_dict.get('Repeat Password')
    if password != repeat_password:
        show_alert_dialog(page, "Passwords do not match")
        return

    hashed_password = hash_password(password)

    return {
        'access_login': fields_dict.get('Access Login'),
        'hash_pass': hashed_password
    }
