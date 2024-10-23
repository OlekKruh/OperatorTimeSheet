from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime, SmallInteger, VARCHAR, Boolean
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    access_login = Column(VARCHAR(15), nullable=False, unique=True)
    hash_pass = Column(VARCHAR(60), comment='for bcrypt', nullable=False)
    is_superuser = Column(Boolean, nullable=False, default=False)


class Operator(Base):
    __tablename__ = 'operator'
    operator_id = Column(Integer, primary_key=True, autoincrement=True)
    operator_name = Column(VARCHAR(12), nullable=False)
    skill = Column(VARCHAR(12), nullable=False)


class Company(Base):
    __tablename__ = 'company'
    company_id = Column(Integer, primary_key=True, autoincrement=True)
    sap_id = Column(VARCHAR, nullable=False, unique=True)
    company_title = Column(VARCHAR(50), nullable=False)
    company_country = Column(VARCHAR(20), nullable=False)
    company_shipping_address = Column(VARCHAR(100), nullable=False)
    company_phone = Column(VARCHAR(20), nullable=False)
    company_email = Column(VARCHAR(50), nullable=False)


class Enclosure(Base):
    __tablename__ = 'enclosure'
    enclosure_id = Column(Integer, primary_key=True, autoincrement=True)
    sap_id = Column(VARCHAR, nullable=False, unique=True)
    enclosure_title = Column(VARCHAR(30), nullable=False)
    base = Column(SmallInteger, nullable=False)
    cover = Column(SmallInteger, nullable=False)
    panel = Column(SmallInteger, nullable=False)
    filter = Column(SmallInteger, nullable=False)
    slot_mask = Column(SmallInteger, nullable=False)
    pcb = Column(SmallInteger, nullable=False)


class Machine(Base):
    __tablename__ = 'machine'
    machine_id = Column(Integer, primary_key=True, autoincrement=True)
    sap_id = Column(VARCHAR, nullable=False, unique=True)
    machine_title = Column(VARCHAR(12), nullable=False, unique=True)
    machine_serial_number = Column(VARCHAR(20), nullable=False, unique=True)
    machine_manufacturer = Column(VARCHAR(50), nullable=False)
    machine_year_production = Column(Date, nullable=False)


class Order(Base):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('company.company_id'), nullable=False)
    enclosure_id = Column(Integer, ForeignKey('enclosure.enclosure_id'), nullable=False)
    variant = Column(VARCHAR(30), nullable=False)
    order_quantity = Column(SmallInteger, nullable=False)
    operation_quantity = Column(SmallInteger, nullable=False)
    operation_description = Column(VARCHAR(250), nullable=False)
    order_cost = Column(Integer, nullable=False)
    order_received_date = Column(Date, nullable=False)

    company = relationship('Company')
    enclosure = relationship('Enclosure')


class TimeSheet(Base):
    __tablename__ = 'time_sheet'
    row_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    operator_id = Column(Integer, ForeignKey('operator.operator_id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    stop_time = Column(DateTime, nullable=False)
    order_id = Column(Integer, ForeignKey('order.order_id'), nullable=False)
    operation = Column(SmallInteger, nullable=False)
    quantity_done = Column(SmallInteger, nullable=False)
    damaged_enclosures = Column(SmallInteger, nullable=False)
    cause_of_damage = Column(VARCHAR(10), nullable=False)
    note_description = Column(VARCHAR(250), nullable=True)
    machine_id = Column(Integer, ForeignKey('machine.machine_id'), nullable=False)

    user = relationship('Users')
    operator = relationship('Operator')
    order = relationship('Order')
    machine = relationship('Machine')


class ChangeLog(Base):
    __tablename__ = 'change_log'
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(VARCHAR(50), nullable=False)
    record_id = Column(Integer, nullable=False)
    operation_type = Column(VARCHAR(10), nullable=False)
    changed_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    old_values = Column(VARCHAR(1000), nullable=False)
    new_values = Column(VARCHAR(1000), nullable=False)

    user = relationship('Users')
