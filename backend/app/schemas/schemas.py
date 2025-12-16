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


# Documento Schemas
class DocumentoBase(BaseModel):
    numeracion_id: int
    estado_id: int
    numero: int
    fecha: date
    base: Decimal
    impuestos: Decimal


class DocumentoCreate(DocumentoBase):
    pass


class DocumentoUpdate(DocumentoBase):
    pass


class DocumentoDetail(DocumentoBase):
    id: int

    class Config:
        from_attributes = True


class Documento(BaseModel):
    numeracion_id: int
    estado_id: int
    numero: int
    fecha: date
    base: Decimal
    impuestos: Decimal

    class Config:
        from_attributes = True


class PaginatedDocumento(BaseModel):
    total: int
    page: int
    size: int
    items: list[Documento]
