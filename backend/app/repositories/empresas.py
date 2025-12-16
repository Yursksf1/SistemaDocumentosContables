from sqlalchemy.orm import Session
from ..models import empresas as ModelsEmpresas
from typing import Optional


# Empresa
def get_empresas(db: Session, page: int = 1, size: Optional[int] = None):
    """Obtener lista de empresas con paginación"""
    query = db.query(ModelsEmpresas.Empresa)
    total = query.count()
    
    if size is None:
        items = query.offset((page - 1) * 10).limit(10).all()
        size = 10
    else:
        items = query.offset((page - 1) * size).limit(size).all()
    
    return total, page, size, items