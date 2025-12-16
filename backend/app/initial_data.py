from sqlalchemy.orm import Session
from .models import models


def init_db(db: Session):
    """Inicializar base de datos con datos de prueba"""
    
    # Verificar si ya existen datos
    existing_country = db.query(models.Empresa).first()
    if existing_country:
        print("Base de datos ya inicializada")
        return
    # aqui se inicia los registros de la base de datos

    db.commit()
    
    print("Base de datos inicializada con éxito")
