from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel  # Para modelos de entrada/salida en la API

# Modelo principal: representa la tabla videojuegos en la BD
class Videojuego(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    genero: str
    lanzamiento: int
    plataforma_id: int

# Modelo para recibir datos al crear o actualizar
class VideojuegoCreate(BaseModel):
    nombre: str
    genero: str
    lanzamiento: int
    plataforma_id: int

# Modelo para devolver datos como respuesta
class VideojuegoResponse(BaseModel):
    id: int
    nombre: str
    genero: str
    lanzamiento: int
    plataforma_id: int

    class Config:
        orm_mode = True  # Necesario para convertir desde el modelo ORM
