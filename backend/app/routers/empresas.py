from ..schemas import empresas as SchemasEmpresas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..controllers import empresas as EmpresasControllers
from ..database import get_db

router = APIRouter()


@router.get("/empresas", response_model=SchemasEmpresas.PaginatedEmpresa)
def get_empresas(db: Session = Depends(get_db)):
    """Obtener todas las empresas"""
    return EmpresasControllers.get_empresas(db)

