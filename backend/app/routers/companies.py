from ..schemas import schemas
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..controllers import crud
from ..database import get_db

router = APIRouter()


@router.get("/empresas", response_model=List[schemas.Empresa])
def get_countries(db: Session = Depends(get_db)):
    """Obtener todos los países"""
    return crud.get_countries(db)

