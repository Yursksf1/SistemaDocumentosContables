from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.documentos import Documento
from typing import Optional


def get_documentos(db: Session, page: int = 1, size: Optional[int] = None):
    """Obtener lista de documentos con paginación"""
    query = db.query(Documento)
    total = query.count()
    
    if size is None:
        items = query.offset((page - 1) * 10).limit(10).all()
        size = 10
    else:
        items = query.offset((page - 1) * size).limit(size).all()
    
    return total, page, size, items


def get_documento_by_id(db: Session, documento_id: int):
    """Obtener un documento por ID"""
    return db.query(Documento).filter(Documento.id == documento_id).first()


def create_documento(db: Session, documento_data: dict):
    """Crear un nuevo documento"""
    db_documento = Documento(**documento_data)
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento


def update_documento(db: Session, documento_id: int, documento_data: dict):
    """Actualizar un documento existente"""
    db_documento = db.query(Documento).filter(Documento.id == documento_id).first()
    if db_documento:
        for key, value in documento_data.items():
            setattr(db_documento, key, value)
        db.commit()
        db.refresh(db_documento)
    return db_documento


def delete_documento(db: Session, documento_id: int):
    """Eliminar un documento"""
    db_documento = db.query(Documento).filter(Documento.id == documento_id).first()
    if db_documento:
        db.delete(db_documento)
        db.commit()
        return True
    return False

def get_documento_by_numeracion_y_numero(db: Session, numeracion_id: int, numero: int):
    """Obtener un documento por numeración y número"""
    return db.query(Documento).filter(
        Documento.numeracion_id == numeracion_id,
        Documento.numero == numero
    ).first()