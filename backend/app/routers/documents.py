from ..schemas import schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..controllers import crud
from ..database import get_db

router = APIRouter()


@router.get("/documentos", response_model=schemas.PaginatedDocumento)
def get_documentos(
    page: int = 1, 
    size: Optional[int] = 10,
    db: Session = Depends(get_db)
):
    """Obtener lista paginada de documentos"""
    if size == -1:
        size = None
    return crud.get_documentos(db, page=page, size=size)


@router.get("/documentos/{documento_id}", response_model=schemas.DocumentoDetail)
def get_documento(documento_id: int, db: Session = Depends(get_db)):
    """Obtener detalle de un documento"""
    documento = crud.get_documento(db, documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return documento


@router.post("/documentos", response_model=schemas.DocumentoCreate)
def create_documento(documento: schemas.DocumentoCreate, db: Session = Depends(get_db)):
    """Crear una nueva documento"""
    return crud.create_documento(db, documento)


@router.put("/documentos/{documento_id}", response_model=schemas.DocumentoUpdate)
def update_documento(
    documento_id: int, 
    documento: schemas.DocumentoUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una documento existente"""
    updated_documento = crud.update_documento(db, documento_id, documento)
    if not updated_documento:
        raise HTTPException(status_code=404, detail="documento no encontrado")
    return updated_documento


@router.delete("/documentos/{documento_id}")
def delete_documento(documento_id: int, db: Session = Depends(get_db)):
    """Eliminar una documento"""
    success = crud.delete_documento(db, documento_id)
    if not success:
        raise HTTPException(status_code=404, detail="documento no encontrado")
    return {"message": "documento eliminado exitosamente"}
