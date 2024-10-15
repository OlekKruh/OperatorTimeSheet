import flet as ft
from .crud_buttons import save_button

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

# User form TextField & list
access_login_field = ft.TextField(label='Access Login', **normal_text_field_style)
password_field = ft.TextField(label='Password', password=True,
                              can_reveal_password=True, **normal_text_field_style)
repeat_password_field = ft.TextField(label='Repeat Password', password=True,
                                     can_reveal_password=True, **normal_text_field_style)

user_form_fields = [
    access_login_field,
    password_field,
    repeat_password_field,
    save_button
]

# Company form TextField & list
company_sap_id = ft.TextField(label='Sap Id', **normal_text_field_style)
company_title = ft.TextField(label='Company Title', **normal_text_field_style)
company_hq_country = ft.TextField(label='Company HQ Country', **normal_text_field_style)
company_shipping_address = ft.TextField(label='Company Shipping Address', **normal_text_field_style)
contact_phone_number = ft.TextField(label='Contact Phone number', **normal_text_field_style)
contact_email = ft.TextField(label='Contact Email', **normal_text_field_style)

company_form_fields = [
    company_sap_id,
    company_title,
    company_hq_country,
    company_shipping_address,
    contact_phone_number,
    contact_email,
    save_button
]

# Enclosure form TextField, Checkbox, Dropdown & list
enclosure_sap_id = ft.TextField(label='Sap Id', **normal_text_field_style)
enclosure_title = ft.TextField(label='Enclosure full Title', **normal_text_field_style)

enclosure_base_checkbox = ft.Checkbox(label='Base', value=True, label_style=enclosure_form_label_style,
                                      fill_color=ft.colors.WHITE)
enclosure_cover_checkbox = ft.Checkbox(label='Cover', value=True, label_style=enclosure_form_label_style,
                                       fill_color=ft.colors.WHITE)
enclosure_filter_checkbox = ft.Checkbox(label='Filter', value=False, label_style=enclosure_form_label_style,
                                        fill_color=ft.colors.WHITE)
enclosure_pcb_checkbox = ft.Checkbox(label='PCB mounting plate', value=False, label_style=enclosure_form_label_style,
                                     fill_color=ft.colors.WHITE)

enclosure_panel_dropdown = ft.Dropdown(
    label='Panel',
    label_style=enclosure_form_label_style,
    options=[ft.dropdown.Option(str(i)) for i in range(3)],
    value='0',
    filled=True,
    fill_color=ft.colors.WHITE,
    text_style=dropdown_text_style,
    bgcolor=ft.colors.WHITE
)

enclosure_slot_mask_dropdown = ft.Dropdown(
    label='Slot Mask',
    label_style=enclosure_form_label_style,
    options=[ft.dropdown.Option(str(i)) for i in range(7)],
    value='0',
    filled=True,
    fill_color=ft.colors.WHITE,
    text_style=dropdown_text_style,
    bgcolor=ft.colors.WHITE
)

enclosure_form_fields = [
    enclosure_sap_id,
    enclosure_title,
    ft.Row(controls=[enclosure_base_checkbox, enclosure_cover_checkbox, enclosure_filter_checkbox,
                     enclosure_pcb_checkbox]),
    ft.Row(controls=[enclosure_panel_dropdown, enclosure_slot_mask_dropdown]),
    save_button
]

# Enclosure form TextField & list
machine_sap_id = ft.TextField(label='Sap Id', **normal_text_field_style)
machine_title = ft.TextField(label='Machine Title', **normal_text_field_style)
machine_serial_number = ft.TextField(label='Machine Serial Number', **normal_text_field_style)
machine_manufacturer = ft.TextField(label='Machine Manufacturer', **normal_text_field_style)
machine_year_production = ft.TextField(label='Machine Year Production Date', **normal_text_field_style)

machine_form_fields = [
    machine_sap_id,
    machine_title,
    machine_serial_number,
    machine_manufacturer,
    machine_year_production,
    save_button
]

# Enclosure form TextField & list
operator_name = ft.TextField(label='Operator Name', **normal_text_field_style)
operator_skill_level = ft.TextField(label='Operator skill level', **normal_text_field_style)
operator_contact_phone = ft.TextField(label='Operator Contact Phone', **normal_text_field_style)

operator_form_fields = [
    operator_name,
    operator_skill_level,
    operator_contact_phone,
    save_button
]

# Enclosure form TextField & list
order_company_id = ft.TextField(label='Company_id', **normal_text_field_style)
order_enclosure_id = ft.TextField(label='Enclosure_id', **normal_text_field_style)
order_variant = ft.TextField(label='Variant', **normal_text_field_style)
order_quantity = ft.TextField(label='Order quantity', **normal_text_field_style)
operations_quantity = ft.TextField(label='Operations quantity', **normal_text_field_style)
operations_descriptions = ft.TextField(label='Operations descriptions', multiline=True, **normal_text_field_style)
order_cost = ft.TextField(label='Order cost in PLN', **normal_text_field_style)

order_form_fields = [
    order_company_id,
    order_enclosure_id,
    order_variant,
    order_quantity,
    operations_quantity,
    operations_descriptions,
    order_cost,
    save_button
]


# Function to return user form fields
def user_form():
    """Returns the form fields for creating or updating a user."""
    return user_form_fields


# Function to return company form fields
def company_form():
    """Returns the form fields for creating or updating a company."""
    return company_form_fields


# Function to return enclosure form fields
def enclosure_form():
    """Returns the form fields for creating or updating an enclosure."""
    return enclosure_form_fields


# Function to return machine form fields
def machine_form():
    """Returns the form fields for creating or updating a machine."""
    return machine_form_fields


# Function to return operator form fields
def operator_form():
    """Returns the form fields for creating or updating an operator."""
    return operator_form_fields


# Function to return order form fields
def order_form():
    """Returns the form fields for creating or updating an order."""
    return order_form_fields
