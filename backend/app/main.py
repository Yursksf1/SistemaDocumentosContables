from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal
from . import models
from .initial_data import init_db
from .routers import companies, documents

# Crear tablas
models.Base.metadata.create_all(bind=engine)

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
app.include_router(companies.router, tags=["Empresas"])
app.include_router(documents.router, tags=["Documentos"])


@app.get("/")
def read_root():
    return {
        "message": "Gestión Personal API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
