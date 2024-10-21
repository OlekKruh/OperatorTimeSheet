import flet as ft

# Field styles
normal_text_field_style = {
    "color": ft.colors.BLACK,
    "bgcolor": ft.colors.WHITE,
    "label_style": ft.TextStyle(color=ft.colors.BLACK, size=12, weight=ft.FontWeight.BOLD),
    "width": 700
}

enclosure_form_label_style = ft.TextStyle(
    color=ft.colors.BLACK,
    size=12,
    weight=ft.FontWeight.BOLD
)

dropdown_text_style = ft.TextStyle(
    color=ft.colors.BLACK,
    size=12,
    weight=ft.FontWeight.BOLD
)

# User form TextField dict
user_form_fields_list = [
    ft.TextField(label='Access Login', **normal_text_field_style),
    ft.TextField(label='Password', password=True,
                 can_reveal_password=True, **normal_text_field_style),
    ft.TextField(label='Repeat Password', password=True,
                 can_reveal_password=True, **normal_text_field_style),
]


# Company form TextField dict
company_form_fields_list = [
    ft.TextField(label='Sap Id', **normal_text_field_style),
    ft.TextField(label='Company title', **normal_text_field_style),
    ft.TextField(label='Company HQ country', **normal_text_field_style),
    ft.TextField(label='Company shipping address', **normal_text_field_style),
    ft.TextField(label='Contact phone number', **normal_text_field_style),
    ft.TextField(label='Contact email', **normal_text_field_style),
]

# Enclosure form TextField, Checkbox, Dropdown dict
enclosure_form_fields_list = [
    ft.TextField(label='Sap Id', **normal_text_field_style),
    ft.TextField(label='Enclosure full Title', **normal_text_field_style),
    ft.Row(controls=[
        ft.Checkbox(label='Base', value=True, label_style=enclosure_form_label_style,
                    fill_color=ft.colors.WHITE),
        ft.Checkbox(label='Cover', value=True, label_style=enclosure_form_label_style,
                    fill_color=ft.colors.WHITE),
        ft.Checkbox(label='Filter', value=False, label_style=enclosure_form_label_style,
                    fill_color=ft.colors.WHITE),
        ft.Checkbox(label='PCB mounting plate', value=False, label_style=enclosure_form_label_style,
                    fill_color=ft.colors.WHITE)
    ]
    ),
    ft.Row(controls=[
        ft.Dropdown(
            label='Panel',
            label_style=enclosure_form_label_style,
            options=[ft.dropdown.Option(str(i)) for i in range(3)],
            value='0',
            filled=True,
            fill_color=ft.colors.WHITE,
            text_style=dropdown_text_style,
            bgcolor=ft.colors.WHITE
        ),
        ft.Dropdown(
            label='Slot Mask',
            label_style=enclosure_form_label_style,
            options=[ft.dropdown.Option(str(i)) for i in range(7)],
            value='0',
            filled=True,
            fill_color=ft.colors.WHITE,
            text_style=dropdown_text_style,
            bgcolor=ft.colors.WHITE
        )
    ]
    ),
]

# Machine form TextField dict
machine_form_fields_list = [
    ft.TextField(label='Sap Id', **normal_text_field_style),
    ft.TextField(label='Machine title', **normal_text_field_style),
    ft.TextField(label='Machine serial number', **normal_text_field_style),
    ft.TextField(label='Machine manufacturer', **normal_text_field_style),
    ft.TextField(label='Machine year production', **normal_text_field_style),
]

# Operator form TextField dict
operator_form_fields_list = [
    ft.TextField(label='Operator Name', **normal_text_field_style),
    ft.TextField(label='Operator skill level', **normal_text_field_style),
    ft.TextField(label='Operator contact phone', **normal_text_field_style),
]

# Order form TextField dict
order_form_fields_list = [
    ft.TextField(label='Company_id', **normal_text_field_style),
    ft.TextField(label='Enclosure_id', **normal_text_field_style),
    ft.TextField(label='Variant', **normal_text_field_style),
    ft.TextField(label='Order quantity', **normal_text_field_style),
    ft.TextField(label='Operations quantity', **normal_text_field_style),
    ft.TextField(label='Operations descriptions', multiline=True, **normal_text_field_style),
    ft.TextField(label='Order cost in PLN', **normal_text_field_style),
    ft.TextField(label='Order received date', **normal_text_field_style),
]


# Function to return user form fields
def user_form():
    """Returns the form fields for creating or updating a user."""
    return user_form_fields_list


# Function to return company form fields
def company_form():
    """Returns the form fields for creating or updating a company."""
    return company_form_fields_list


# Function to return enclosure form fields
def enclosure_form():
    """Returns the form fields for creating or updating an enclosure."""
    return enclosure_form_fields_list


# Function to return machine form fields
def machine_form():
    """Returns the form fields for creating or updating a machine."""
    return machine_form_fields_list


# Function to return operator form fields
def operator_form():
    """Returns the form fields for creating or updating an operator."""
    return operator_form_fields_list


# Function to return order form fields
def order_form():
    """Returns the form fields for creating or updating an order."""
    return order_form_fields_list
