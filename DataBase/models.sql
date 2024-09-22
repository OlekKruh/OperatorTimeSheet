from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Date, DateTime, SmallInteger, VARCHAR
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    user_id = Column(Integer, primary_key=True)
    access_login = Column(VARCHAR(15))
    hash_pass = Column(String(60), comment='for bcrypt')

class Operator(Base):
    __tablename__ = 'Operator'
    operator_id = Column(Integer, primary_key=True)
    operator_name = Column(String(12))
    position = Column(String(12))

class Company(Base):
    __tablename__ = 'Company'
    company_id = Column(Integer, primary_key=True)
    sap_id = Column(String)
    company_title = Column(String(50))
    company_country = Column(String(20))
    company_shipping_address = Column(String(100))
    company_phone = Column(Integer)
    company_email = Column(String(50))

class Enclosure(Base):
    __tablename__ = 'Enclosure'
    enclosure_id = Column(Integer, primary_key=True)
    sap_id = Column(String)
    enclosure_title = Column(String(30))

class Machine(Base):
    __tablename__ = 'Machine'
    machine_id = Column(Integer, primary_key=True)
    sap_id = Column(String)
    machine_title = Column(String(12))
    machine_serial_number = Column(String(20))
    machine_manufacturer = Column(String(50))
    machine_year_production = Column(Date)

class Order(Base):
    __tablename__ = 'Order'
    order_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('Company.company_id'))
    enclosure_id = Column(Integer, ForeignKey('Enclosure.enclosure_id'))
    variant = Column(String(30))
    order_quantity = Column(SmallInteger)
    processing_sides = Column(SmallInteger)
    processing_sides_description = Column(Text)
    order_cost = Column(Integer)

    company = relationship('Company')
    enclosure = relationship('Enclosure')

class TimeSheet(Base):
    __tablename__ = 'TimeSheet'
    row_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    operator_id = Column(Integer, ForeignKey('Operator.operator_id'))
    start_time = Column(DateTime)
    stop_time = Column(DateTime)
    order_id = Column(Integer, ForeignKey('Order.order_id'))
    processing_side = Column(SmallInteger)
    quantity_done = Column(SmallInteger)
    note_description = Column(Text)
    machine_id = Column(Integer, ForeignKey('Machine.machine_id'))

    user = relationship('User')
    operator = relationship('Operator')
    order = relationship('Order')
    machine = relationship('Machine')

class ChangeLog(Base):
    __tablename__ = 'ChangeLog'
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(50))
    operation_type = Column(String(10))
    record_id = Column(Integer)
    changed_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('User.user_id'))
    old_values = Column(Text)
    new_values = Column(Text)

    user = relationship('User')

# Пример создания базы данных
# engine = create_engine('postgresql://user:password@localhost/mydatabase')
# Base.metadata.create_all(engine)
