from sqlmodel import SQLModel, Field  # SQLModel para definir el modelo de la tabla, Field para definir columnas
from typing import Optional  # Para indicar que el ID puede ser opcional
from pydantic import BaseModel  # Para los modelos que se usan en la entrada y salida de la API

# Este es el modelo principal que representa la tabla "videojuegos" en la base de datos
class Videojuego(SQLModel, table=True):  # table=True indica que es una tabla real en SQLite
    id: Optional[int] = Field(default=None, primary_key=True)  # ID autoincremental como clave primaria
    nombre: str  # Nombre del videojuego
    genero: str  # Género (ej. acción, aventura...)
    lanzamiento: int  # Año de lanzamiento
    plataforma_id: int  # Relación con la plataforma (llave foránea)

# Modelo que uso para recibir datos cuando se va a crear o actualizar un videojuego
class VideojuegoCreate(BaseModel):
    nombre: str
    genero: str
    lanzamiento: int
    plataforma_id: int

# Modelo que uso para devolver los datos como respuesta desde la API
class VideojuegoResponse(BaseModel):
    id: int
    nombre: str
    genero: str
    lanzamiento: int
    plataforma_id: int

    class Config:
        orm_mode = True  #

    class Config:
        orm_mode = True  # Esto permite que la respuesta entienda los datos que vienen del modelo ORM
