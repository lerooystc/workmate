from db.base import Base
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.sql import func


class Trade(Base):
    __tablename__ = "spimex_trading_results"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    exchange_product_id = Column(String, nullable=False, comment="ID продукта")
    exchange_product_name = Column(String, nullable=False, comment="Название продукта")
    oil_id = Column(String, nullable=False, comment="ID нефти")
    delivery_basis_id = Column(String, nullable=False, comment="ID базиса")
    delivery_basis_name = Column(String, nullable=False, comment="Название базиса")
    delivery_type_id = Column(String, nullable=False, comment="ID типа доставки")
    volume = Column(Integer, nullable=False, comment="Объем")
    total = Column(Integer, nullable=False, comment="Общая сумма")
    count = Column(Integer, nullable=False, comment="Кол-во")
    date = Column(Date, nullable=False, comment="Дата торгов")
    created_on = Column(DateTime, server_default=func.now(), comment="Дата создания")
    updated_on = Column(
        DateTime, onupdate=func.now(), comment="Дата последнего обновления"
    )
