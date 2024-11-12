from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class CreateTrade(BaseModel):
    exchange_product_id: str = Field(..., description="ID продукта")
    exchange_product_name: str = Field(..., description="Название продукта")
    oil_id: str = Field(..., description="ID нефти")
    delivery_basis_id: str = Field(..., description="ID базиса")
    delivery_basis_name: str = Field(..., description="Название базиса")
    delivery_type_id: str = Field(..., description="ID типа доставки")
    volume: int = Field(..., description="Объем")
    total: int = Field(..., description="Общая сумма")
    count: int = Field(..., description="Кол-во")
    date: date = Field(..., description="Дата торгов")
    created_on: datetime = Field(..., description="Дата создания")
    updated_on: datetime = Field(..., description="Дата последнего обновления")
