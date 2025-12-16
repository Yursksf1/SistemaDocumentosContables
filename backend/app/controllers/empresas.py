from sqlalchemy.orm import Session
from typing import Optional
from ..repositories import empresas as RepositoriesEmpresas


# Empresas
def get_empresas(db: Session, page: int = 1, size: Optional[int] = None):
    total, page, size, items = RepositoriesEmpresas.get_empresas(db, page, size)
    return {"total": total, "page": page, "size": size, "items": items}