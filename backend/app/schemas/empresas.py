from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import Optional


# Empresa Schemas
class Empresa(BaseModel):
    id: int
    identificacion: str
    razon_social: str

    class Config:
        from_attributes = True


class PaginatedEmpresa(BaseModel):
    total: int
    page: int
    size: int
    items: list[Empresa]
