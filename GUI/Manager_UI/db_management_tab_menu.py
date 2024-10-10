import flet as ft

name = 'DB manager'


def db_management_tab_menu(user_role: str):
    """
    Creates the DB Manager tab menu. Tabs “Users” and “ChangeLog”
    are visible only for users with roles 'admin' or 'superuser'.

     Args:
        user_role: The role of the logged-in user ('admin', 'superuser', 'manager', 'operator').
    """

    # Function to generate scrollable content for each tab
    def tab_content(tab_name):
        return ft.Container(
            content=ft.Column(
                controls=[ft.Text(f"{tab_name} content line {i}") for i in range(50)],  # Example long content
                scroll=ft.ScrollMode.AUTO  # Enable scroll if content exceeds available height
            ),
            expand=True  # Allow the content to expand to the container size
        )

    # Create a list of tabs that are always visible
    tabs = [
        ft.Tab(
            text='Order',
            content=tab_content("Order"),
            icon=ft.icons.BORDER_COLOR,
        ),
        ft.Tab(
            text='Enclosure',
            content=tab_content("Enclosure"),
            icon=ft.icons.ALL_INBOX,
        ),
        ft.Tab(
            text='TimeSheet',
            content=tab_content("TimeSheet"),
            icon=ft.icons.TABLE_ROWS_ROUNDED,
        ),
        ft.Tab(
            text='Companies',
            content=tab_content("Companies management in progress"),
            icon=ft.icons.HOME_WORK_SHARP,
        ),
        ft.Tab(
            text='Operators',
            content=tab_content("Operators management in progress"),
            icon=ft.icons.PEOPLE_SHARP,
        ),
        ft.Tab(
            text='Machines',
            content=tab_content("Machine management in progress"),
            icon=ft.icons.DRAW
        ),
    ]

    # If the user is 'admin' or 'superuser', add the "Users" and "ChangeLog" tabs
    if user_role in ['admin', 'super_user']:
        tabs.append(
            ft.Tab(
                text='Users',
                content=tab_content("Users"),
                icon=ft.icons.PERSON,
            )
        )
        tabs.append(
            ft.Tab(
                text='ChangeLog',
                content=tab_content("ChangeLog"),
                icon=ft.icons.HISTORY,
            )
        )

    # Return the Tabs component with the appropriate tabs
    return ft.Tabs(
        selected_index=0,
        animation_duration=400,
        tabs=tabs,
        expand=True,
        indicator_color=ft.colors.GREEN_ACCENT_400,
        divider_color=ft.colors.WHITE,
        label_color=ft.colors.GREEN_ACCENT_400,
    )
