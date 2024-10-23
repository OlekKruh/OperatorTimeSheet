import flet as ft
from sqlalchemy.orm import Session


def load_data_from_db(model, session: Session):
    """
    Загружает данные из базы данных для заданной модели.

    Args:
        model: Модель SQLAlchemy, на основе которой строится таблица.
        session: Сессия SQLAlchemy для выполнения запросов.

    Returns:
        list: Список записей модели.
    """
    try:
        # Загружаем все записи модели
        records = session.query(model).all()
        return records
    except Exception as e:
        print(f"Error loading data: {e}")
        return []


def create_data_table_automatically(model, session: Session):
    """
    Автоматически создает DataTable на основе модели SQLAlchemy.

    Args:
        model: Модель SQLAlchemy, на основе которой строится таблица.
        session: Сессия SQLAlchemy для выполнения запросов.

    Returns:
        ft.DataTable: Таблица данных Flet.
    """
    # Загружаем все записи из таблицы модели
    records = load_data_from_db(model, session)

    # Извлекаем имена колонок из модели
    columns = [
        ft.DataColumn(ft.Text(column.name))  # Автоматически используем имя колонки из модели
        for column in model.__table__.columns
    ]

    # Создаем строки данных, извлекая значения атрибутов из каждой записи
    rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(getattr(record, column.name))))
                for column in model.__table__.columns
            ]
        )
        for record in records
    ]

    # Возвращаем готовую таблицу
    return ft.DataTable(columns=columns, rows=rows)

# def create_tables(model, session: Session):
#     """Создаёт таблицу данных для модели."""
#     # Загружаем данные из БД
#     records = load_data_from_db(model, session)
#
#     match model:
#         case "Users":
#             columns = [
#                 ft.DataColumn(ft.Text("User id")),
#                 ft.DataColumn(ft.Text("Access login")),
#                 ft.DataColumn(ft.Text("Hash")),
#             ]
#             return columns
#         case "Operator":
#             columns = [
#                 ft.DataColumn(ft.Text("Operator id")),
#                 ft.DataColumn(ft.Text("Name")),
#                 ft.DataColumn(ft.Text("Skill")),
#             ]
#             return columns
#         case "Company":
#             columns = [
#                 ft.DataColumn(ft.Text("Company id")),
#                 ft.DataColumn(ft.Text("Sap id")),
#                 ft.DataColumn(ft.Text("Title")),
#                 ft.DataColumn(ft.Text("Country")),
#                 ft.DataColumn(ft.Text("Shipping address")),
#                 ft.DataColumn(ft.Text("Contact phone")),
#                 ft.DataColumn(ft.Text("Email")),
#             ]
#             return columns
#         case "Enclosure":
#             columns = [
#                 ft.DataColumn(ft.Text("Enclosure id")),
#                 ft.DataColumn(ft.Text("Sap id")),
#                 ft.DataColumn(ft.Text("Title")),
#                 # ft.DataColumn(ft.Text("Material")),
#                 ft.DataColumn(ft.Text("Base")),
#                 ft.DataColumn(ft.Text("Cover")),
#                 ft.DataColumn(ft.Text("Panel")),
#                 ft.DataColumn(ft.Text("Filter")),
#                 ft.DataColumn(ft.Text("Slot mask")),
#                 ft.DataColumn(ft.Text("PCB mount plate")),
#             ]
#             return columns
#         case "Machine":
#             columns = [
#                 ft.DataColumn(ft.Text("Machine id")),
#                 ft.DataColumn(ft.Text("Sap id")),
#                 ft.DataColumn(ft.Text("Title")),
#                 ft.DataColumn(ft.Text("Serial number")),
#                 ft.DataColumn(ft.Text("Manufacturer")),
#                 ft.DataColumn(ft.Text("Production year")),
#             ]
#             return columns
#         case "Order":
#             columns = [
#                 ft.DataColumn(ft.Text("Order id")),
#                 ft.DataColumn(ft.Text("Company id")),
#                 ft.DataColumn(ft.Text("Enclosure id")),
#                 ft.DataColumn(ft.Text("Variant")),
#                 ft.DataColumn(ft.Text("Order quantity")),
#                 ft.DataColumn(ft.Text("Operations quantity")),
#                 ft.DataColumn(ft.Text("Operation description")),
#                 ft.DataColumn(ft.Text("Order cost")),
#                 ft.DataColumn(ft.Text("Order received date")),
#             ]
#             return columns
#         case "TimeSheet":
#             columns = [
#                 ft.DataColumn(ft.Text("Row id")),
#                 ft.DataColumn(ft.Text("User id")),
#                 ft.DataColumn(ft.Text("Operator id")),
#                 ft.DataColumn(ft.Text("Start time")),
#                 ft.DataColumn(ft.Text("Stop time")),
#                 ft.DataColumn(ft.Text("Order id")),
#                 ft.DataColumn(ft.Text("Operation")),
#                 ft.DataColumn(ft.Text("Quantity done")),
#                 ft.DataColumn(ft.Text("Damaged enclosures")),
#                 ft.DataColumn(ft.Text("Cause of damage")),
#                 ft.DataColumn(ft.Text("Note")),
#                 ft.DataColumn(ft.Text("Machine id")),
#             ]
#             return columns
#         case "ChangeLog":
#             columns = [
#                 ft.DataColumn(ft.Text("log id")),
#                 ft.DataColumn(ft.Text("Table name")),
#                 ft.DataColumn(ft.Text("Record id")),
#                 ft.DataColumn(ft.Text("Operation type")),
#                 ft.DataColumn(ft.Text("Changed at")),
#                 ft.DataColumn(ft.Text("User id")),
#                 ft.DataColumn(ft.Text("Old values")),
#                 ft.DataColumn(ft.Text("New values")),
#             ]
#             return columns

