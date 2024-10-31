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
    exchange_product_id = Column(String, unique=True, nullable=False)
    exchange_product_name = Column(String, nullable=False)
    oil_id = Column(String, nullable=False)
    delivery_basis_id = Column(String, nullable=False)
    delivery_basis_name = Column(String, nullable=False)
    delivery_type_id = Column(String, nullable=False)
    volume = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, onupdate=func.now())
