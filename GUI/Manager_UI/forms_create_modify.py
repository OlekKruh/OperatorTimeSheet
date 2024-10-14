import flet as ft

normal_text_field_style = {
    "color": ft.colors.BLACK,
    "bgcolor": ft.colors.WHITE,
    "label_style": ft.TextStyle(color=ft.colors.BLACK, size=12, weight=ft.FontWeight.BOLD),
    "width": 700
}

save_buton = ft.FilledButton(
    text='Save',
    on_click=None,
    style=ft.ButtonStyle(
        color=ft.colors.BLACK,
        bgcolor=ft.colors.WHITE,

    )
)


def user_form():
    fields = [
        ft.TextField(label='Access Login', **normal_text_field_style),
        ft.TextField(label='Password', password=True, can_reveal_password=True, **normal_text_field_style),
        ft.TextField(label='Repeat Password', password=True, can_reveal_password=True, **normal_text_field_style),
        save_buton
    ]
    return fields


def company_form():
    fields = [
        ft.TextField(label='Sap Id', **normal_text_field_style),
        ft.TextField(label='Company Title', **normal_text_field_style),
        ft.TextField(label='Company HQ Country', **normal_text_field_style),
        ft.TextField(label='Company Shipping Address', **normal_text_field_style),
        ft.TextField(label='Contact Phone number', **normal_text_field_style),
        ft.TextField(label='Contact Email', **normal_text_field_style),
        save_buton
    ]
    return fields


def enclosure_form():
    fields = [
        ft.TextField(label='Sap Id', **normal_text_field_style),
        ft.TextField(label='Enclosure full Title', **normal_text_field_style),
        ft.TextField(label='Base', **normal_text_field_style),
        ft.TextField(label='Cover', **normal_text_field_style),
        ft.TextField(label='Panel', **normal_text_field_style),
        ft.TextField(label='Filter', **normal_text_field_style),
        ft.TextField(label='Slot Mask', **normal_text_field_style),
        ft.TextField(label='PCB mounting plate', **normal_text_field_style),
        save_buton
    ]
    return fields


def machine_form():
    fields = [
        ft.TextField(label='Sap Id', **normal_text_field_style),
        ft.TextField(label='Machine Title', **normal_text_field_style),
        ft.TextField(label='Machine Serial Number', **normal_text_field_style),
        ft.TextField(label='Machine Manufacturer', **normal_text_field_style),
        ft.TextField(label='Machine Year Production Date', **normal_text_field_style),
        save_buton
    ]
    return fields


def operator_form():
    fields = [
        ft.TextField(label='Operator Name', **normal_text_field_style),
        ft.TextField(label='Operator skill level', **normal_text_field_style),
        ft.TextField(label='Operator Contact Phone', **normal_text_field_style),
        save_buton
    ]
    return fields


def order_form():
    fields = [
        ft.TextField(label='Company_id', **normal_text_field_style),
        ft.TextField(label='Enclosure_id', **normal_text_field_style),
        ft.TextField(label='Variant', **normal_text_field_style),
        ft.TextField(label='Order quantity', **normal_text_field_style),
        ft.TextField(label='Operations quantity', **normal_text_field_style),
        ft.TextField(label='Operations descriptions', multiline=True, **normal_text_field_style),
        ft.TextField(label='Order cost in PLN', **normal_text_field_style),
        save_buton
    ]
    return fields
