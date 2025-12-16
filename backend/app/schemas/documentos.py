from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import Optional

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

class DocumentoPatch(BaseModel):
    numeracion_id: Optional[int] = None
    estado_id: Optional[int] = None
    fecha: Optional[date] = None
    base: Optional[Decimal] = None
    impuestos: Optional[Decimal] = None

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


# Estadísticas Schemas
class EstadisticaItem(BaseModel):
    """Schema para un item individual de resultado de estadística"""
    
    class Config:
        from_attributes = True


class EstadisticaResponse(BaseModel):
    """Schema para una estadística completa con su título y resultados"""
    titulo: str
    result: list[dict]


class EstadisticasDocumentosResponse(BaseModel):
    """Schema para el response completo de estadísticas de documentos"""
    estadisticas: list[EstadisticaResponse]
