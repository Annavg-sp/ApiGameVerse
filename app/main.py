from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database.database import engine  # Motor de la base de datos
from app.routes import plataformas, videojuegos, auth  # Importo las rutas
from app.database.models.apikey import API_Keys  # Modelo para las claves API

# Creo la instancia principal de FastAPI
app = FastAPI(
    title="GameVerse.API",
    version="1.0.0",
    description="Conéctate con el mundo de los videojuegos a través de GameVerse.API"
)

# Crea todas las tablas automáticamente
SQLModel.metadata.create_all(engine)

# Reemplazo el esquema OpenAPI de FastAPI por el mío personalizado (sin candado global)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Reemplazo el esquema OpenAPI de FastAPI por el mío personalizado
app.openapi = custom_openapi

# Incluyo las rutas de los distintos recursos
app.include_router(videojuegos.router, prefix="/videojuegos", tags=["Videojuegos"])  # Solo videojuegos tienen el candado
app.include_router(plataformas.router, prefix="/plataformas", tags=["Plataformas"])
app.include_router(auth.router)  # Ruta de login/registro va sin prefijo

# Ruta principal de bienvenida
@app.get("/")
async def index():
    return {
        "success": True,
        "data": {
            "endpoints": ["/videojuegos", "/plataformas", "/auth"]
        }
    }
