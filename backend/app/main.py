from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal
from .models import documentos as documentosModels, empresas as empresasModels
from .initial_data import init_db
from .routers import empresas, documentos

# Crear tablas
empresasModels.Base.metadata.create_all(bind=engine)
documentosModels.Base.metadata.create_all(bind=engine)

# Inicializar datos
db = SessionLocal()
try:
    init_db(db)
finally:
    db.close()

app = FastAPI(
    title="Gestión de Documentos API",
    description="API para gestión de documentos contables autorizados por la DIAN",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(empresas.router, tags=["Empresas"])
app.include_router(documentos.router, tags=["Documentos"])


@app.get("/")
def read_root():
    return {
        "message": "Gestión de documentos API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
