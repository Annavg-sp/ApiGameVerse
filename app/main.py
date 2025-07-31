from fastapi import FastAPI  # Importamos FastAPI para crear la app
from sqlmodel import SQLModel  # Usamos SQLModel para manejar los modelos y la BD
from app.database.database import engine  # Motor de conexión a la base de datos
from app.routes import plataformas, videojuegos  # Importamos las rutas

# Modelos que aseguran la creación de tablas en la BD
from app.database.models.videojuego import Videojuego
from app.database.models.plataforma import Plataforma

# Creamos la instancia de la app
app = FastAPI(
    title="GameVerse.API",
    version="1.0.0",
    description="Conéctate con el mundo de los videojuegos a través de GameVerse.API"
)

# Se crean las tablas si no existen
SQLModel.metadata.create_all(engine)

# Se incluyen las rutas separadas por recursos
app.include_router(videojuegos.router, prefix="/videojuegos", tags=["Videojuegos"])
app.include_router(plataformas.router, prefix="/plataformas", tags=["Plataformas"])

# Ruta principal que muestra los endpoints disponibles
@app.get("/")
async def index():
    return {
        "success": True,
        "data": {
            "endpoints": ["/videojuegos", "/plataformas"]
        }
    }
