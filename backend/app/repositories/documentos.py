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


# Estadísticas
def get_empresas_con_mas_fallidos_que_exitosos(db: Session):
    """
    Obtener empresas que tienen más documentos fallidos que exitosos
    Basado en query_1.sql
    """
    from sqlalchemy import case, func
    from ..models.empresas import Empresa, Numeracion
    from ..models.documentos import Estado
    
    query = db.query(
        Empresa.id,
        Empresa.razon_social
    ).join(
        Numeracion, Empresa.id == Numeracion.empresa_id
    ).join(
        Documento, Numeracion.id == Documento.numeracion_id
    ).join(
        Estado, Documento.estado_id == Estado.id
    ).group_by(
        Empresa.id,
        Empresa.razon_social
    ).having(
        func.sum(case((~Estado.exitoso, 1), else_=0)) >
        func.sum(case((Estado.exitoso, 1), else_=0))
    )
    
    results = query.all()
    return [{"id": r.id, "razon_social": r.razon_social} for r in results]


def get_cantidad_documentos_por_tipo_entre_fechas(db: Session, fecha_inicio: str, fecha_fin: str):
    """
    Obtener cantidad de facturas, notas débito y notas crédito emitidas entre dos fechas
    Basado en query_2.sql
    """
    from sqlalchemy import func
    from ..models.documentos import TipoDocumento
    from ..models.empresas import Numeracion
    
    query = db.query(
        TipoDocumento.descripcion,
        func.count().label('cantidad')
    ).join(
        Numeracion, TipoDocumento.id == Numeracion.tipo_documento_id
    ).join(
        Documento, Numeracion.id == Documento.numeracion_id
    ).filter(
        Documento.fecha >= fecha_inicio,
        Documento.fecha <= fecha_fin
    ).group_by(
        TipoDocumento.descripcion
    )
    
    results = query.all()
    return [{"descripcion": r.descripcion, "cantidad": r.cantidad} for r in results]


def get_cantidad_documentos_por_estado_y_empresa(db: Session):
    """
    Obtener cantidad de documentos por estado, agrupada por empresa
    Basado en query_3.sql
    """
    from sqlalchemy import func
    from ..models.empresas import Empresa, Numeracion
    from ..models.documentos import Estado
    
    query = db.query(
        Empresa.razon_social,
        Estado.descripcion,
        func.count().label('cantidad')
    ).join(
        Numeracion, Empresa.id == Numeracion.empresa_id
    ).join(
        Documento, Numeracion.id == Documento.numeracion_id
    ).join(
        Estado, Documento.estado_id == Estado.id
    ).group_by(
        Empresa.razon_social,
        Estado.descripcion
    ).order_by(
        Empresa.razon_social,
        Estado.descripcion
    )
    
    results = query.all()
    return [{"razon_social": r.razon_social, "estado": r.descripcion, "cantidad": r.cantidad} for r in results]


def get_empresas_con_mas_de_n_documentos_fallidos(db: Session, n: int = 3):
    """
    Obtener empresas con más de N documentos no exitosos
    Basado en query_4.sql
    """
    from sqlalchemy import case, func
    from ..models.empresas import Empresa, Numeracion
    from ..models.documentos import Estado
    
    query = db.query(
        Empresa.razon_social,
        func.sum(case((~Estado.exitoso, 1), else_=0)).label('numero_fallidos')
    ).join(
        Numeracion, Empresa.id == Numeracion.empresa_id
    ).join(
        Documento, Numeracion.id == Documento.numeracion_id
    ).join(
        Estado, Documento.estado_id == Estado.id
    ).group_by(
        Empresa.razon_social
    ).having(
        func.sum(case((~Estado.exitoso, 1), else_=0)) > n
    )
    
    results = query.all()
    return [{"razon_social": r.razon_social, "numero_fallidos": r.numero_fallidos} for r in results]


def get_documentos_fuera_de_rango(db: Session):
    """
    Obtener documentos cuyo número o fecha esté fuera del rango o vigencia autorizada
    Basado en query_5.sql
    """
    from sqlalchemy import or_
    from ..models.empresas import Numeracion
    
    query = db.query(
        Documento.id,
        Documento.numero,
        Documento.fecha
    ).join(
        Numeracion, Documento.numeracion_id == Numeracion.id
    ).filter(
        or_(
            Documento.numero < Numeracion.consecutivo_inicial,
            Documento.numero > Numeracion.consecutivo_final,
            Documento.fecha < Numeracion.vigencia_inicial,
            Documento.fecha > Numeracion.vigencia_final
        )
    )
    
    results = query.all()
    return [{"id": r.id, "numero": r.numero, "fecha": str(r.fecha)} for r in results]


def get_total_dinero_por_empresa(db: Session):
    """
    Obtener total dinero recibido por empresa (facturas, notas débito) no se incluyen notas crédito
    Basado en query_6.sql
    """
    from sqlalchemy import func
    from ..models.empresas import Empresa, Numeracion
    from ..models.documentos import TipoDocumento
    
    # Primero obtenemos los IDs de Factura de Venta y Nota Débito
    tipos_ids_query = db.query(TipoDocumento.id).filter(
        TipoDocumento.descripcion.in_(['Factura de Venta', 'Nota Débito'])
    )
    
    query = db.query(
        Empresa.razon_social,
        func.sum(Documento.base + Documento.impuestos).label('total_recibido')
    ).join(
        Numeracion, Empresa.id == Numeracion.empresa_id
    ).join(
        Documento, Numeracion.id == Documento.numeracion_id
    ).filter(
        Numeracion.tipo_documento_id.in_(tipos_ids_query)
    ).group_by(
        Empresa.razon_social
    )
    
    results = query.all()
    return [{"razon_social": r.razon_social, "total_recibido": float(r.total_recibido) if r.total_recibido else 0} for r in results]


def get_numeros_repetidos_por_empresa(db: Session):
    """
    Detectar números completos repetidos (prefijo + número) en cada empresa
    Basado en query_7.sql
    """
    from sqlalchemy import func
    from ..models.empresas import Empresa, Numeracion
    
    query = db.query(
        Empresa.razon_social,
        Numeracion.prefijo,
        Documento.numero,
        func.count().label('cantidad_repetidos')
    ).join(
        Numeracion, Empresa.id == Numeracion.empresa_id
    ).join(
        Documento, Numeracion.id == Documento.numeracion_id
    ).group_by(
        Empresa.razon_social,
        Numeracion.prefijo,
        Documento.numero
    ).having(
        func.count() > 1
    )
    
    results = query.all()
    return [{"razon_social": r.razon_social, "prefijo": r.prefijo, "numero": r.numero, "cantidad_repetidos": r.cantidad_repetidos} for r in results]
