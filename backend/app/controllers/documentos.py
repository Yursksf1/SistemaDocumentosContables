from sqlalchemy.orm import Session
from typing import Optional
from ..schemas import documentos
from ..repositories import documentos as DocumentosRepository
from ..repositories import empresas as EmpresasRepository
from fastapi import HTTPException
from datetime import date


# Funciones auxiliares de validación
def _validar_valores_monetarios(valor_base: float, impuesto: float):
    """Validar que los valores monetarios sean correctos"""
    if valor_base <= 0:
        raise HTTPException(status_code=400, detail="El valor base debe ser mayor a 0")
    
    if impuesto <= 0:
        raise HTTPException(status_code=400, detail="El impuesto debe ser mayor a 0")
    
    if impuesto >= valor_base:
        raise HTTPException(status_code=400, detail="El impuesto no puede ser mayor al valor base")


def _validar_numeracion_y_rango(db: Session, numeracion_id: int, numero: int, fecha: date):
    """Validar que la numeración exista y el número esté en el rango autorizado"""
    numeracion = EmpresasRepository.get_numeracion_by_id(db, numeracion_id)
    if not numeracion:
        raise HTTPException(status_code=404, detail="Numeración no encontrada")
    
    if numero < numeracion.consecutivo_inicial or numero > numeracion.consecutivo_final:
        raise HTTPException(
            status_code=400, 
            detail=f"El número {numero} está fuera del rango autorizado ({numeracion.consecutivo_inicial}-{numeracion.consecutivo_final})"
        )
    
    if numeracion.vigencia_inicial and fecha < numeracion.vigencia_inicial:
        raise HTTPException(status_code=400, detail="La numeración aún no está vigente")
    
    if numeracion.vigencia_final and fecha > numeracion.vigencia_final:
        raise HTTPException(status_code=400, detail="La numeración ya no está vigente")
    
    return True

    

def _validar_numero_no_duplicado(db: Session, numeracion_id: int, numero: int, documento_id: Optional[int] = None):
    """Validar que el número no haya sido usado previamente en la numeración"""
    documento_existente = DocumentosRepository.get_documento_by_numeracion_y_numero(
        db, numeracion_id, numero
    )
    
    if documento_existente and (documento_id is None or documento_existente.id != documento_id):
        raise HTTPException(
            status_code=400, 
            detail=f"El número {numero} ya fue usado en esta numeración"
        )


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
    # Validaciones de negocio
    _validar_valores_monetarios(documento.valor_base, documento.impuesto)
    _validar_numeracion_y_rango(db, documento.numeracion_id, documento.numero, documento.fecha)
    _validar_numero_no_duplicado(db, documento.numeracion_id, documento.numero)
    
    documento_data = documento.model_dump()
    return DocumentosRepository.create_documento(db, documento_data)

def update_documento(db: Session, documento_id: int, documento: documentos.DocumentoUpdate):
    """Actualizar un documento"""
    _validar_valores_monetarios(documento.valor_base, documento.impuesto)
    _validar_numeracion_y_rango(db, documento.numeracion_id, documento.numero, documento.fecha)
    _validar_numero_no_duplicado(db, documento.numeracion_id, documento.numero, documento_id)
    
    documento_data = documento.model_dump()
    return DocumentosRepository.update_documento(db, documento_id, documento_data)

def patch_documento(db: Session, documento_id: int, documento: documentos.DocumentoPatch):
    """Actualizar parcialmente un documento"""
    # TODO: Add validations for patched fields
    
    documento_data = documento.model_dump(exclude_unset=True)
    return DocumentosRepository.update_documento(db, documento_id, documento_data)

def delete_documento(db: Session, documento_id: int):
    """Eliminar un documento"""
    return DocumentosRepository.delete_documento(db, documento_id)
