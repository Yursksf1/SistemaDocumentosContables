from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Numeric, UniqueConstraint
from ..database import Base


class TipoDocumento(Base):
    __tablename__ = "tipo_documento"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(256))


class Estado(Base):
    __tablename__ = "estado"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(256))
    exitoso = Column(Boolean)


class Documento(Base):
    __tablename__ = "documento"

    id = Column(Integer, primary_key=True, index=True)
    numeracion_id = Column(Integer, ForeignKey("numeracion.id"))
    estado_id = Column(Integer, ForeignKey("estado.id"))
    numero = Column(Integer, index=True)
    fecha = Column(Date)
    base = Column(Numeric(10, 2))
    impuestos = Column(Numeric(10, 2))

    __table_args__ = (
        UniqueConstraint('numero', 'numeracion_id', name='uq_numero_numeracion'),
    )