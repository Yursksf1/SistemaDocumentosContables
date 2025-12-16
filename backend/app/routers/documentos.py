from ..schemas import documentos as SchemasDocumentos
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..controllers import documentos as ControllerDocumentos
from ..database import get_db

router = APIRouter()


@router.get("/documentos", response_model=SchemasDocumentos.PaginatedDocumento)
def get_documentos(
    page: int = 1, 
    size: Optional[int] = 10,
    db: Session = Depends(get_db)
):
    """Obtener lista paginada de documentos"""
    if size == -1:
        size = None
    return ControllerDocumentos.get_documentos(db, page=page, size=size)


@router.get("/documentos/{documento_id}", response_model=SchemasDocumentos.DocumentoDetail)
def get_documento(documento_id: int, db: Session = Depends(get_db)):
    """Obtener detalle de un documento"""
    documento = ControllerDocumentos.get_documento(db, documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return documento


@router.post("/documentos", response_model=SchemasDocumentos.DocumentoCreate)
def create_documento(documento: SchemasDocumentos.DocumentoCreate, db: Session = Depends(get_db)):
    """Crear una nueva documento"""
    return ControllerDocumentos.create_documento(db, documento)


@router.put("/documentos/{documento_id}", response_model=SchemasDocumentos.DocumentoUpdate)
def update_documento(
    documento_id: int, 
    documento: SchemasDocumentos.DocumentoUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una documento existente"""
    updated_documento = ControllerDocumentos.update_documento(db, documento_id, documento)
    if not updated_documento:
        raise HTTPException(status_code=404, detail="documento no encontrado")
    return updated_documento


@router.delete("/documentos/{documento_id}")
def delete_documento(documento_id: int, db: Session = Depends(get_db)):
    """Eliminar una documento"""
    success = ControllerDocumentos.delete_documento(db, documento_id)
    if not success:
        raise HTTPException(status_code=404, detail="documento no encontrado")
    return {"message": "documento eliminado exitosamente"}
