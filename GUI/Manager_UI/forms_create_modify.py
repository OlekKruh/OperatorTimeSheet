import flet as ft

text_field_style = {
    # "border_color": ft.colors.WHITE,
    "color": ft.colors.BLACK,
    "bgcolor": ft.colors.WHITE,
    "label_style": ft.TextStyle(color=ft.colors.GREY_500, size=12, weight=ft.FontWeight.BOLD),
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
        ft.TextField(label='Access Login', **text_field_style),
        ft.TextField(label='Password', password=True, can_reveal_password=True, **text_field_style),
        ft.TextField(label='Repeat Password', password=True, can_reveal_password=True, **text_field_style),
        save_buton
    ]
    return fields


def company_form():
    fields = [
        ft.TextField(label='Sap Id', **text_field_style),
        ft.TextField(label='Company Title', **text_field_style),
        ft.TextField(label='Company HQ Country', **text_field_style),
        ft.TextField(label='Company Shipping Address', **text_field_style),
        ft.TextField(label='Contact Phone number', **text_field_style),
        ft.TextField(label='Contact Email', **text_field_style),
        save_buton
    ]
    return fields


def enclosure_form():
    fields = [
        ft.TextField(label='Sap Id', **text_field_style),
        ft.TextField(label='Enclosure full Title', **text_field_style),
        # add checkboxes for enclosure parts and appearance text fields with values.
        save_buton
    ]
    return fields


def machine_form():
    fields = [
        ft.TextField(label='Sap Id', **text_field_style),
        ft.TextField(label='Machine Title', **text_field_style),
        ft.TextField(label='Machine Serial Number', **text_field_style),
        ft.TextField(label='Machine Manufacturer', **text_field_style),
        ft.TextField(label='Machine Year Production Date', **text_field_style),
        save_buton
    ]
    return fields


def operator_form():
    fields = [
        ft.TextField(label='Operator Name', **text_field_style),
        ft.TextField(label='Operator skill level', **text_field_style),
        ft.TextField(label='Operator Contact Phone', **text_field_style),
        save_buton
    ]
    return fields


def order_form():
    fields = [
        ft.TextField(label='Company_id', **text_field_style),
        ft.TextField(label='Enclosure_id', **text_field_style),
        ft.TextField(label='Variant', **text_field_style),
        ft.TextField(label='Order quantity', **text_field_style),
        ft.TextField(label='Operations quantity', **text_field_style),
        ft.TextField(label='Operations descriptions', multiline=True, **text_field_style),
        ft.TextField(label='Order cost in PLN', **text_field_style),
        save_buton
    ]
    return fields
