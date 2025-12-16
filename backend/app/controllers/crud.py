from ..schemas import schemas
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models
from typing import Optional


# Empresa
def get_empresas(db: Session):
    return db.query(models.Empresa).all()


# Documento
def get_documentos(db: Session, page: int = 1, size: Optional[int] = None):
    query = db.query(models.Documento)
    total = query.count()

    if size is None or size <= 0:
        # Return all
        items = query.order_by(models.Documento.id).all()
        return {"total": total, "page": 1, "size": total, "items": items}

    offset = (page - 1) * size
    items = query.order_by(models.Documento.id).offset(offset).limit(size).all()

    return {"total": total, "page": page, "size": size, "items": items}


def get_documento(db: Session, documento_id: int):
    return db.query(models.Documento).filter(models.Documento.id == documento_id).first()


def create_documento(db: Session, documento: schemas.DocumentoCreate):
    db_documento = models.Documento(**documento.model_dump())
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento


def update_documento(db: Session, documento_id: int, documento: schemas.DocumentoUpdate):
    db_documento = db.query(models.Documento).filter(models.Documento.id == documento_id).first()
    if db_documento:
        for key, value in documento.model_dump().items():
            setattr(db_documento, key, value)
        db.commit()
        db.refresh(db_documento)
    return db_documento


def delete_documento(db: Session, documento_id: int):
    db_documento = db.query(models.Documento).filter(models.Documento.id == documento_id).first()
    if db_documento:
        db.delete(db_documento)
        db.commit()
        return True
    return False
