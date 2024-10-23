import flet as ft

# Поля стилей
NORMAL_TEXT_FIELD_STYLE = {
    "color": ft.colors.BLACK,
    "bgcolor": ft.colors.WHITE,
    "label_style": ft.TextStyle(color=ft.colors.BLACK, size=12, weight=ft.FontWeight.BOLD),
    "width": 600,
}

ENCLOSURE_FORM_LABEL_STYLE = ft.TextStyle(
    color=ft.colors.BLACK,
    size=12,
    weight=ft.FontWeight.BOLD
)

DROPDOWN_TEXT_STYLE = ft.TextStyle(
    color=ft.colors.BLACK,
    size=12,
    weight=ft.FontWeight.BOLD
)


# Функция для создания текстовых полей с заданными параметрами
def create_text_field(label, password=False, multiline=False, can_reveal_password=False):
    return ft.TextField(
        label=label,
        password=password,
        can_reveal_password=can_reveal_password,
        multiline=multiline,
        expand=False,
        **NORMAL_TEXT_FIELD_STYLE
    )


# Пользовательские поля формы
user_form_fields_list = [
    create_text_field('Access Login'),
    create_text_field('Password', password=True, can_reveal_password=True),
    create_text_field('Repeat Password', password=True, can_reveal_password=True)
]

# Поля формы компании
company_form_fields_list = [
    create_text_field('Sap Id'),
    create_text_field('Company title'),
    create_text_field('Company HQ country'),
    create_text_field('Company shipping address'),
    create_text_field('Contact phone number'),
    create_text_field('Contact email')
]

# Поля формы корпуса
enclosure_form_fields_list = [
    create_text_field('Sap Id'),
    create_text_field('Enclosure full Title'),
    ft.Row(controls=[
        ft.Checkbox(label='Base', value=True, label_style=ENCLOSURE_FORM_LABEL_STYLE, fill_color=ft.colors.WHITE),
        ft.Checkbox(label='Cover', value=True, label_style=ENCLOSURE_FORM_LABEL_STYLE, fill_color=ft.colors.WHITE),
        ft.Checkbox(label='Filter', value=False, label_style=ENCLOSURE_FORM_LABEL_STYLE, fill_color=ft.colors.WHITE),
        ft.Checkbox(label='PCB mounting plate', value=False, label_style=ENCLOSURE_FORM_LABEL_STYLE,
                    fill_color=ft.colors.WHITE)
    ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    ),
    ft.Row(controls=[
        ft.Dropdown(
            label='Panel',
            label_style=ENCLOSURE_FORM_LABEL_STYLE,
            options=[ft.dropdown.Option(str(i)) for i in range(3)],
            value='0',
            filled=True,
            fill_color=ft.colors.WHITE,
            text_style=DROPDOWN_TEXT_STYLE,
            bgcolor=ft.colors.WHITE,
            width=150,
        ),
        ft.Dropdown(
            label='Slot Mask',
            label_style=ENCLOSURE_FORM_LABEL_STYLE,
            options=[ft.dropdown.Option(str(i)) for i in range(7)],
            value='0',
            filled=True,
            fill_color=ft.colors.WHITE,
            text_style=DROPDOWN_TEXT_STYLE,
            bgcolor=ft.colors.WHITE,
            width=150,
        )
    ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
]

# Поля формы машины
machine_form_fields_list = [
    create_text_field('Sap Id'),
    create_text_field('Machine title'),
    create_text_field('Machine serial number'),
    create_text_field('Machine manufacturer'),
    create_text_field('Machine year production')
]

# Поля формы оператора
operator_form_fields_list = [
    create_text_field('Operator Name'),
    create_text_field('Operator skill level')
]

# Поля формы заказа
order_form_fields_list = [
    create_text_field('Company_id'),
    create_text_field('Enclosure_id'),
    create_text_field('Variant'),
    create_text_field('Order quantity'),
    create_text_field('Operations quantity'),
    create_text_field('Operations descriptions', multiline=True),
    create_text_field('Order cost in PLN'),
    create_text_field('Order received date')
]


# Функции для возврата полей форм
def user_form():
    """Returns the form fields for creating or updating a user."""
    return user_form_fields_list


def company_form():
    """Returns the form fields for creating or updating a company."""
    return company_form_fields_list


def enclosure_form():
    """Returns the form fields for creating or updating an enclosure."""
    return enclosure_form_fields_list


def machine_form():
    """Returns the form fields for creating or updating a machine."""
    return machine_form_fields_list


def operator_form():
    """Returns the form fields for creating or updating an operator."""
    return operator_form_fields_list


def order_form():
    """Returns the form fields for creating or updating an order."""
    return order_form_fields_list
