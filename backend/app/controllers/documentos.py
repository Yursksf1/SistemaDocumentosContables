from sqlalchemy.orm import Session
from typing import Optional
from ..schemas import documentos
from ..repositories import documentos as DocumentosRepository


# Documento
def get_documentos(db: Session, page: int = 1, size: Optional[int] = None):
    """Obtener lista de documentos con paginación"""
    total, page, size, items = DocumentosRepository.get_documentos(db, page, size)
    return {"total": total, "page": page, "size": size, "items": items}


def get_documento(db: Session, documento_id: int):
    """Obtener un documento por ID"""
    return DocumentosRepository.get_documento_by_id(db, documento_id)


def create_documento(db: Session, documento: documentos.DocumentoCreate):
    """Crear un nuevo documento"""
    documento_data = documento.model_dump()
    return DocumentosRepository.create_documento(db, documento_data)


def update_documento(db: Session, documento_id: int, documento: documentos.DocumentoUpdate):
    """Actualizar un documento"""
    documento_data = documento.model_dump()
    return DocumentosRepository.update_documento(db, documento_id, documento_data)


def delete_documento(db: Session, documento_id: int):
    """Eliminar un documento"""
    return DocumentosRepository.delete_documento(db, documento_id)
