from sqlmodel import SQLModel, Field  # SQLModel para definir las tablas y Field para las columnas
from typing import Optional  # Usado para campos que son opcionales
from pydantic import BaseModel  # Usado para modelos de entrada/salida en la API

# Modelo principal que representa la tabla "plataformas" en la base de datos
class Plataforma(SQLModel, table=True):  # table=True indica que es una tabla de la base de datos
    id: Optional[int] = Field(default=None, primary_key=True)  # ID autoincremental como clave primaria
    nombre: str  # Nombre de la plataforma (ej. PlayStation, Xbox...)
    fabricante: str  # Fabricante de la plataforma (ej. Sony, Microsoft...)

# Modelo para crear nuevas plataformas (entrada de datos)
class PlataformaCreate(BaseModel):
    nombre: str
    fabricante: str

# Modelo para devolver las plataformas como respuesta en la API
class PlataformaResponse(BaseModel):
    id: int
    nombre: str
    fabricante: str

    class Config:
        orm_mode = True  # Esto convierte el modelo ORM (base de datos) a un modelo Pydantic para la API
