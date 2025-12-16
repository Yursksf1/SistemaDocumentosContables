from sqlalchemy.orm import Session
from .models import empresas, documentos
from datetime import date, timedelta
import random


def init_db(db: Session):
    """Inicializar base de datos con datos de prueba"""
    
    # Verificar si ya existen datos
    existing_empresa = db.query(empresas.Empresa).first()
    if existing_empresa:
        print("Base de datos ya inicializada")
        return
    
    # Crear 3 empresas
    empresas_list = [
        empresas.Empresa(identificacion="900123456", razon_social="Avicampo Santander S.A.S"),
        empresas.Empresa(identificacion="900234567", razon_social="Corona Colombia S.A.S"),
        empresas.Empresa(identificacion="900345678", razon_social="Leonisa S.A.S")
    ]
    for empresa in empresas_list:
        db.add(empresa)
    db.flush()
    
    # Crear 3 tipos de documentos
    tipos_documento = [
        documentos.TipoDocumento(descripcion="Factura de Venta"),
        documentos.TipoDocumento(descripcion="Nota Débito"),
        documentos.TipoDocumento(descripcion="Nota Crédito")
    ]
    for tipo in tipos_documento:
        db.add(tipo)
    db.flush()
    
    # Crear 7 estados
    estados_list = [
        documentos.Estado(descripcion="Emitido", exitoso=True),
        documentos.Estado(descripcion="Aceptado", exitoso=True),
        documentos.Estado(descripcion="Aprobado por DIAN", exitoso=True),
        documentos.Estado(descripcion="Rechazado", exitoso=False),
        documentos.Estado(descripcion="Error de Validación", exitoso=False),
        documentos.Estado(descripcion="Anulado", exitoso=False),
        documentos.Estado(descripcion="En Proceso", exitoso=True)
    ]
    for estado in estados_list:
        db.add(estado)
    db.flush()
    
    # Crear 6 numeraciones por empresa (18 total)
    numeraciones_list = []
    prefijos = ["FV", "ND", "NC"]
    fecha_inicial = date(2025, 1, 1)
    fecha_final = date(2025, 12, 31)
    
    for empresa in empresas_list:
        for i, tipo in enumerate(tipos_documento):
            # Crear 2 numeraciones por tipo de documento para cada empresa
            numeracion1 = empresas.Numeracion(
                tipo_documento_id=tipo.id,
                empresa_id=empresa.id,
                prefijo=f"{prefijos[i]}01",
                consecutivo_inicial=1,
                consecutivo_final=1000,
                vigencia_inicial=fecha_inicial,
                vigencia_final=fecha_final
            )
            numeracion2 = empresas.Numeracion(
                tipo_documento_id=tipo.id,
                empresa_id=empresa.id,
                prefijo=f"{prefijos[i]}02",
                consecutivo_inicial=1001,
                consecutivo_final=2000,
                vigencia_inicial=fecha_inicial,
                vigencia_final=fecha_final
            )
            db.add(numeracion1)
            db.add(numeracion2)
            numeraciones_list.extend([numeracion1, numeracion2])
    db.flush()
    
    # Crear 6 documentos por numeración (108 total)
    contador = 0
    for numeracion in numeraciones_list:
        consecutivo_actual = numeracion.consecutivo_inicial
        for i in range(6):
            # Asegurar que el número esté dentro del rango permitido
            if consecutivo_actual > numeracion.consecutivo_final:
                break
            
            numero = consecutivo_actual
            fecha_doc = fecha_inicial + timedelta(days=contador * 2)
            
            # Alternar entre diferentes estados
            estado_idx = contador % len(estados_list)
            
            # Generar valores base e impuestos variados
            base = round(random.uniform(20000, 500000), 2)
            impuestos = round(base * 0.19, 2)
            
            documento = documentos.Documento(
                numeracion_id=numeracion.id,
                estado_id=estados_list[estado_idx].id,
                numero=numero,
                fecha=fecha_doc,
                base=base,
                impuestos=impuestos
            )
            db.add(documento)
            contador += 1
            consecutivo_actual += 1
    
    db.flush()
    
    db.commit()
    
    print("Base de datos inicializada con éxito")
    print(f"- {len(empresas_list)} empresas creadas")
    print(f"- {len(tipos_documento)} tipos de documento creados")
    print(f"- {len(estados_list)} estados creados")
    print(f"- {len(numeraciones_list)} numeraciones creadas")
    print(f"- {contador} documentos creados")
