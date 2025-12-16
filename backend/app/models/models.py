from sqlalchemy import Column, Integer, String, Date, ForeignKey, Decimal, Boolean
from sqlalchemy.orm import relationship
from ..database import Base


class Empresa(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, index=True)
    identificacion = Column(String(16))
    razon_social = Column(String(256))


class TipoDocumento(Base):
    __tablename__ = "tipo_documento"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(256))


class Numeracion(Base):
    __tablename__ = "numeracion"

    id = Column(Integer, primary_key=True, index=True)
    tipo_documento_id = Column(Integer, ForeignKey("tipo_documento.id"))
    empresa_id = Column(Integer, ForeignKey("empresa.id"))
    prefijo = Column(String(8))
    consecutivo_inicial = Column(Integer)
    consecutivo_final = Column(Integer)
    vigencia_inicial = Column(Date)
    vigencia_final = Column(Date)


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
    numero = Column(Integer, unique=True, index=True)
    fecha = Column(Date)
    base = Column(Decimal)
    impuestos = Column(Decimal)
