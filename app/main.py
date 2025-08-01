from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database.database import engine
from app.routes import plataformas, videojuegos, auth
from app.database.models.apikey import API_Keys

app = FastAPI(
    title="GameVerse.API",
    version="1.0.0",
    description="Conéctate con el mundo de los videojuegos a través de GameVerse.API"
)

# Crear todas las tablas
SQLModel.metadata.create_all(engine)

# Añadir esquema de seguridad para Swagger (candado Bearer)
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

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer"
        }
    }

    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Incluir las rutas 
app.include_router(videojuegos.router, prefix="/videojuegos", tags=["Videojuegos"])
app.include_router(plataformas.router, prefix="/plataformas", tags=["Plataformas"])
app.include_router(auth.router)  # Auth no necesita prefijo adicional

#Ruta de bienvenida
@app.get("/")
async def index():
    return {
        "success": True,
        "data": {
            "endpoints": ["/videojuegos", "/plataformas", "/auth"]
        }
    }
